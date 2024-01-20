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
    form_data = request.data

    email_body = (
        'Expense Form Submission\n\n'
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

    logo_file = form_data.get('logo')
    print(f"Logo path: {logo_file}")

    if isinstance(logo_file, InMemoryUploadedFile):

        # This path will change once I impleement the churches app!
        logo_path = "/tmp/" + logo_file.name
        print(f"New logo path: {logo_path}")

        # Add the logo path to the form data.
        form_data['logo'] = logo_path

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
    email = EmailMessage(
        'Expense Form submission by ' + form_data['name'],
        email_body,
        settings.DEFAULT_FROM_EMAIL,
        ['csernus.szilvi@gmail.com']
    )

    # Create the final PDF and close the merger.
    final_buffer = BytesIO()
    pdf_merge.write(final_buffer)

    # Attach the final PDF to the email.
    email.attach("attachment.pdf", final_buffer.getvalue(), "application/pdf")

    email.send()

    final_buffer.close()
    pdf_merge.close()

    return Response(status=200, data={"message": "Email sent."})
