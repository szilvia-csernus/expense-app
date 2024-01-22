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
from churches.models import Church
import os


# Open the file, if it's an image, resize if necessary and convert it to PDF
# return a buffer with the PDF data.
def process_file(file, max_size):
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

    else:
        print(f"Unsupported file type: {file.content_type}")
        return None

    buffer.seek(0)
    return buffer


@api_view(['POST'])
def send_expense_form(request):
    counter_obj = get_object_or_404(ClaimsCounter, pk=1)
    counter = str(counter_obj.counter)
    form_data = request.data

    form_data['counter'] = counter
    church_name = form_data['church']
    logo = get_object_or_404(Church, name=church_name).logo
    form_data['logo'] = logo.url

    main_message = (
        'Name: ' + form_data['name'] + '\n' +
        'Email: ' + form_data['email'] + '\n' +
        'Church: ' + form_data['church'] + '\n' +
        'Purpose: ' + form_data['purpose'] + '\n' +
        'Date of Expense: ' + form_data['date'] + '\n' +
        'Description: ' + form_data['description'] + '\n' +
        'Total: ' + form_data['total'] + '\n' +
        'Bank account: ' + form_data['iban'] + '\n' +
        'Name of Bank Account Holder: ' + form_data['accountName'] + '\n\n'
    )

    message_to_submitter = (
        'Dear ' + form_data['name'] + ', \n\n' +
        'Thank you for submitting an expense form. We will process ' +
        'it shortly.' + '\n' +
        "If you don't hear from us, or if the reimbursement doesn't arrive " +
        'to you within 2 weeks, then please reach out to us at ' +
        os.environ['FINANCE_EMAIL'] + '.\n\n' +

        'Attila' + '\n' +
        'Finance Team' + '\n' +
        'Redeemer International Church Rotterdam' + '\n\n' +

        'Ps - the submitted data:' + '\n\n' +
        main_message
    )

    message_to_finance = (
        'Expense Form Submission' + '\n\n' +
        main_message
    )

    # Create a file-like buffer to receive PDF data.
    form_buffer = BytesIO()

    # Generate the PDF from the form HTML and add the pdf to the buffer.
    try:
        html_content = render_to_string('email-template.html', form_data)
        pisa.CreatePDF(html_content, dest=form_buffer)
        form_buffer.seek(0)
    except Exception as e:
        print(f"Error generating PDF: {e}")
        return Response(status=500, data={"message": "Error generating PDF."})

    # The merger pdf will merge this and the upcoming PDF receipts together.
    pdf_merge = PdfWriter()
    pdf_merge.append(form_buffer)
    form_buffer.close()

    # Read the receipts, convert them to PDF, and add them to the merger.
    i = 0
    while True:
        receipt_field = 'receipt' + str(i)
        receipt_file = form_data.get(receipt_field)
        if receipt_file is None:
            break

        try:
            max_size = (2480, 3507)  # Maximum size for A4 paper at 300 DPI
            receipt_buffer = process_file(receipt_file, max_size)
            pdf_merge.append(receipt_buffer)
            receipt_buffer.close()

        except Exception as e:
            print(f"Error processing receipt {i}: {e}")

        i += 1

    # Create the email message.
    subject = 'Expense Form ' + counter + ' - ' + form_data['purpose']
    email_acknowledgement = EmailMessage(
        subject,
        message_to_submitter,
        settings.DEFAULT_FROM_EMAIL,
        [form_data['email']]
    )

    email_to_finance = EmailMessage(
        subject,
        message_to_finance,
        settings.DEFAULT_FROM_EMAIL,
        [os.environ['FINANCE_EMAIL']]
    )

    # Create the final PDF and close the merger.
    final_buffer = BytesIO()
    pdf_merge.write(final_buffer)

    # Attach the final PDF to the emails an send them.
    attachment_name = 'EF' + counter + '.pdf'
    email_to_finance.attach(attachment_name,
                            final_buffer.getvalue(), "application/pdf")
    email_to_finance.send()
    email_acknowledgement.attach(attachment_name,
                                 final_buffer.getvalue(), "application/pdf")
    email_acknowledgement.send()

    final_buffer.close()
    pdf_merge.close()

    # After the email has been sent, increment the counter
    counter_obj.increment()

    return Response(status=200, data={"message": "Email sent."})
