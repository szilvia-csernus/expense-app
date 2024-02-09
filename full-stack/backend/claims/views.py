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
from .forms import ExpenseForm, ImageUploads
from churches.models import Church
import os


def validate_form(request):
    """
    Validate the form and the images. Return a 400 response if the form is
    invalid, or if any of the images are invalid. Return None if everything is
    valid.
    """
    form = ExpenseForm(request.data)
    if not form.is_valid():
        return Response(status=400, data=form.errors)

    receipts = [ImageUploads({'image': request.FILES.get(name)})
                for name in request.FILES
                if name.startswith('receipt')]

    if not all(f.is_valid() for f in receipts):
        return Response(status=400, data={"message": "Invalid image file."})

    return None


def process_file(file, max_size):
    """
    Open the file, if it's an image, resize if necessary and convert it to PDF.
    Return a buffer with the PDF data.
    """
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
    validate_form(request)
    counter_obj = get_object_or_404(ClaimsCounter, pk=1)
    counter = str(counter_obj.counter)
    form = request.data

    form['counter'] = counter
    church_name = form['church']
    logo = get_object_or_404(Church, name=church_name).logo
    form['logo'] = logo.url

    main_message = (
        'Name: ' + form['name'] + '\n' +
        'Email: ' + form['email'] + '\n' +
        'Church: ' + form['church'] + '\n' +
        'Purpose: ' + form['purpose'] + '\n' +
        'Date of Expense: ' + form['date'] + '\n' +
        'Description: ' + form['description'] + '\n' +
        'Total: ' + form['total'] + '\n' +
        'Bank account: ' + form['iban'] + '\n' +
        'Name of Bank Account Holder: ' + form['accountName'] + '\n\n'
    )

    message_to_submitter = (
        'Dear ' + form['name'] + ', \n\n' +
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
        html_content = render_to_string('email-template.html', form)
        pisa.CreatePDF(html_content, dest=form_buffer)
        form_buffer.seek(0)
    except Exception as e:
        print(f"Error generating PDF: {e}")
        return Response(status=500, data={"message": "Unfortunately, we were \
                                          unable to process the PDF file you \
                                          sent us. Please try taking a picture\
                                           of it instead."})

    # The merger pdf will merge this and the upcoming PDF receipts together.
    pdf_merge = PdfWriter()
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
            pdf_merge.append(receipt_buffer)
            receipt_buffer.close()

        except Exception as e:
            print(f"Error processing receipt {i}: {e}")

        i += 1

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
