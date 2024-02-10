# from django.core.mail import send_mail
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image as PilImage
from django.template.loader import render_to_string
from pypdf import PdfWriter
from io import BytesIO
from django.core.mail import EmailMessage
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from xhtml2pdf import pisa
from django.shortcuts import get_object_or_404
from .models import ClaimsCounter
from .serializers import ExpenseSerializer, ReceiptUploadsSerializer
from churches.models import Church
import os


def validate_form(request):
    """
    Validate the form and the images. Return a 400 response if the form is
    invalid, or if any of the images are invalid. Return None if everything is
    valid.
    """
    form = ExpenseSerializer(data=request.data)
    if not form.is_valid():
        return Response(status=400, data=form.errors)

    receipts = [ReceiptUploadsSerializer(
        data={'receipt': request.FILES.get(name)})
                for name in request.FILES
                if name.startswith('receipt')]

    if not all(f.is_valid() for f in receipts):
        return Response(status=400, data={"message": "Invalid image file."})

    return None


def update_form_with_additional_data(request, counter):
    """
    Append additional data to the form, such as the counter, the church's name,
    and the logo's URL.
    """
    form = request.data

    form['counter'] = counter
    church_name = form['church']
    logo = get_object_or_404(Church, name=church_name).logo
    form['logo'] = logo.url
    return form


def generate_main_message(form):
    """
    Generate the main message for the email, using the form data.
    """
    return (
        f"Name: {form['name']}\n"
        f"Email: {form['email']}\n"
        f"Church: {form['church']}\n"
        f"Purpose: {form['purpose']}\n"
        f"Date of Expense: {form['date']}\n"
        f"Description: {form['description']}\n"
        f"Total: {form['total']}\n"
        f"Bank account: {form['iban']}\n"
        f"Name of Bank Account Holder: {form['accountName']}\n\n"
    )


def generate_message_to_submitter(form, main_message):
    """
    Generate the message to the submitter, using the form data.
    """
    return (
        f"Dear {form['name']}, \n\n"
        f"Thank you for submitting an expense form. "
        f"We will process it shortly.\n"
        f"If you don't hear from us, or if the reimbursement doesn't arrive "
        f"to you within 2 weeks, then please reach out to us at "
        f"{os.environ['FINANCE_EMAIL']}.\n\n"
        f"Attila\n"
        f"Finance Team\n"
        f"Redeemer International Church Rotterdam\n\n"
        f"Ps - the submitted data:\n\n" +
        main_message
    )


def generate_message_to_finance(form, main_message):
    """
    Generate the message to the finance team, using the form data.
    """
    return (
        "Expense Form Submission\n\n" +
        main_message
    )


def process_file(file, max_size):
    """
    Open the file, if it's an image, resize if necessary and convert it to PDF.
    Return a buffer with the PDF data. Expecting valid image or pdf files.
    """
    # Create a file-like buffer for the form to receive PDF data.
    buffer = BytesIO()

    if file.content_type.startswith('image/'):
        if isinstance(file, InMemoryUploadedFile):
            # It's an image. Open it with PIL and resize it.
            image = PilImage.open(file)
            image.thumbnail(max_size)

            # Convert the image to PDF and write it to a buffer.
            image.save(buffer, 'PDF')
            image.close()

    elif file.content_type == 'application/pdf':
        # It's a PDF. Write it directly to the buffer.
        buffer.write(file.read())

    buffer.seek(0)
    return buffer


def generate_form_pdf(form):
    """
    Generate HTML from the form data, convert it to PDF and add it to the
    buffer. Return the buffer.
    """
    # Create a file-like buffer for the form to receive PDF data.
    buffer = BytesIO()
    try:
        html_content = render_to_string('email-template.html', form)
        pisa.CreatePDF(html_content, dest=buffer)
        buffer.seek(0)
    except Exception as e:
        print(f"Error generating PDF: {e}")
        return Response(status=500, data={"message": "Unfortunately, we were \
                                          unable to process the PDF file you \
                                          sent us. Please try taking a picture\
                                           of it instead."})

    buffer.seek(0)
    return buffer


def generate_attachement(form):
    # The merger pdf will merge the generated PDFs together.
    pdf_merge = PdfWriter()

    # Generate the PDF from the form and add the pdf to the form_buffer. If the
    # form_buffer is a Response, meaning there was an error, return this
    # response.
    form_buffer = generate_form_pdf(form)
    if isinstance(form_buffer, Response):
        return form_buffer

    pdf_merge.append(form_buffer)
    form_buffer.close()

    # Read the receipts, convert them to PDF, and add them to the merger.
    i = 0
    while True:
        receipt_field = 'receipt' + str(i)
        receipt_file = form.get(receipt_field)
        if receipt_file is None:
            break

        try:
            max_size = (700, 1100)
            receipt_buffer = process_file(receipt_file, max_size)
            if receipt_buffer is not None:
                pdf_merge.append(receipt_buffer)
                receipt_buffer.close()

        except Exception as e:
            print(f"Error processing receipt {i}: {e}")
            return Response(status=500, data={"message": "Unfortunately, we \
                                          are unable to process one or more \
                                          image(s) you sent us. Please \
                                          try another format."})

        i += 1

    return pdf_merge


@api_view(['POST'])
def send_expense_form(request):
    # Validate the form and the images, and return a 400 response if invalid.
    form_validation_response = validate_form(request)
    if isinstance(form_validation_response, Response):
        return form_validation_response

    # Retrieve the counter from the database.
    counter_obj = get_object_or_404(ClaimsCounter, pk=1)
    counter = str(counter_obj.counter)

    # Update the form with data retrieved from the database.
    form = update_form_with_additional_data(request, counter)

    # Construct the text messages for the emails.
    main_message = generate_main_message(form)
    message_to_submitter = generate_message_to_submitter(form, main_message)
    message_to_finance = generate_message_to_finance(form, main_message)

    # Construct the PDF attachment. If the attachment is a Response, meaning
    # there was an error, return this response to the user.
    attachement = generate_attachement(form)
    if isinstance(attachement, Response):
        return attachement

    # Create the email message.
    subject = 'Expense Form ' + counter + ' - ' + form['purpose']
    email_acknowledgement = EmailMessage(
        subject,
        message_to_submitter,
        settings.DEFAULT_FROM_EMAIL,
        [form['email']]
    )

    email_to_finance = EmailMessage(
        subject,
        message_to_finance,
        settings.DEFAULT_FROM_EMAIL,
        [os.environ['FINANCE_EMAIL']]
    )

    # Create the final PDF and close the merger.
    buffer_for_attachement = BytesIO()
    attachement.write(buffer_for_attachement)

    # Attach the final PDF to the emails an send them.
    attachment_name = 'EF' + counter + '.pdf'
    email_to_finance.attach(attachment_name,
                            buffer_for_attachement.getvalue(),
                            "application/pdf")
    email_to_finance.send()
    email_acknowledgement.attach(attachment_name,
                                 buffer_for_attachement.getvalue(),
                                 "application/pdf")
    email_acknowledgement.send()

    buffer_for_attachement.close()
    attachement.close()

    # After the email has been sent, increment the counter
    counter_obj.increment()

    print(f"Email sent for expense form {counter} to {form['email']} and \
          {os.environ['FINANCE_EMAIL']}")
    return Response(status=200, data={"message": "Email sent."})
