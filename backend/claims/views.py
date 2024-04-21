from django.views.decorators.csrf import csrf_protect
from django.db import transaction
from django.core.mail import EmailMessage
from django.conf import settings
from django.shortcuts import get_object_or_404

from rest_framework.decorators import api_view
from rest_framework.response import Response

from io import BytesIO

from cost_centers.models import Church
import logging

from .utils import validate_form, generate_attachment, generate_main_message, generate_message_to_submitter, generate_message_to_finance, generate_reply_template


@csrf_protect
@api_view(['POST'])
def send_expense_form(request):
    # Initialize the logger.
    logger = logging.getLogger(__name__)

    # Validate the form and the images, return a 400 response if invalid.
    form_validation_response = validate_form(request)
    if isinstance(form_validation_response, Response):
        logger.error("Form validation failed: ")
        logger.error(form_validation_response.data)
        return Response(status=form_validation_response.status_code)

    form = request.data

    # Retrieve the church from the database.
    church = get_object_or_404(Church, short_name=form['church'])
    if church.finance_email is None:
        return Response(status=400, data={
            "message": "Error retrieving church data."})

    counter = str(church.claims_counter)

    # Append the logo_url and the counter to the form.
    form['logo'] = church.logo.url if church.logo else ""
    form['counter'] = counter

    # Construct the text messages for the emails.
    main_message = generate_main_message(form)
    message_to_submitter = generate_message_to_submitter(church,
                                                         form['name'])
    message_to_finance = generate_message_to_finance(main_message)
    message_template = generate_reply_template(church,
                                               form['name'],
                                               main_message)

    # Construct the PDF attachment. If the attachment_response is a Response
    # object, meaning there was an error, return this response to the user.
    attachment_response = generate_attachment(form)
    if isinstance(attachment_response, Response):
        logger.error(attachment_response.data)
        return attachment_response
    else:
        attachment = attachment_response

    # Create the email messages.
    subject_for_submitter = 'Expense Form ' + counter + ' '\
                            + form['description'] + ' ' + form['purpose']
    email_acknowledgement = EmailMessage(
        subject_for_submitter,
        message_to_submitter,
        settings.DEFAULT_FROM_EMAIL,
        [form['email']],
        reply_to=[church.finance_email]
    )

    subject_for_finance = 'EF ' + counter + ' '\
                          + form['description'] + ' ' + form['purpose']
    email_to_finance = EmailMessage(
        subject_for_finance,
        message_to_finance,
        settings.DEFAULT_FROM_EMAIL,
        [church.finance_email],
        reply_to=[form['email']]
    )

    subject_for_template = 'Expense Form ' + counter + ' '\
                           + form['description'] + ' ' + form['purpose']
    email_template = EmailMessage(
        subject_for_template,
        message_template,
        settings.DEFAULT_FROM_EMAIL,
        [church.finance_email],
        reply_to=[form['email']]
    )

    try:
        # Create the final PDF and close the merger.
        buffer_for_attachment = BytesIO()
        attachment.write(buffer_for_attachment)

        # Attach the final PDF to the emails an send them.
        attachment_name = 'EF' + counter + '.pdf'
        email_to_finance.attach(attachment_name,
                                buffer_for_attachment.getvalue(),
                                "application/pdf")
        email_to_finance.send()

        email_acknowledgement.send()

        email_template.send()

        # After the email has been sent, increment the counter
        with transaction.atomic():
            church.refresh_from_db()
            church.increment_claims_counter()

    except Exception as e:
        logger.error(f"Error sending email from name: {form['name']}, \
            email: {form['email']}. Error: {e}")
        return Response(status=406, data={
            "message": "Error sending email. Please try again."})

    finally:
        # This code will be executed whether an exception occurs or not
        buffer_for_attachment.close()
        attachment.close()

    logger.warning(
        f"Email sent for expense form {counter} to {form['email']}" +
        f" and finance team: {church.finance_email}.")
    return Response(status=200)
