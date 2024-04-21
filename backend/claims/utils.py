from django.core.files.uploadedfile import InMemoryUploadedFile
from django.template.loader import render_to_string
from rest_framework.response import Response

from PIL import Image as PilImage, ImageOps
from pypdf import PdfWriter
from io import BytesIO
from xhtml2pdf import pisa

from .serializers import ExpenseSerializer, ReceiptUploadsSerializer

import logging


# limit the log level of xhtml2pdf to ERROR
logging.getLogger('xhtml2pdf').setLevel(logging.ERROR)


def validate_form(request):
    """
    Validate the form and the images. Return a 400 response if the form is
    invalid, or if any of the images are invalid. Return None if everything is
    valid.
    """
    form = ExpenseSerializer(data=request.data)
    if not form.is_valid():
        return Response(status=400, data={
            "message":
                f"Escaped Frontend validation: form.errors {form.errors}"})

    if not request.FILES:
        return Response(
          status=400, data={
            "message": "Escaped Frontend validation: File upload required."})

    max_total_size = 5.1 * 1024 * 1024  # 5.1 MB

    total_size = sum(file.size for file in request.FILES.values())
    if total_size > max_total_size:
        return Response(
            status=400,
            data={
                "message": ("Escaped Frontend validation: "
                            "The total size of all files exceeds the limit.")
            }
        )

    receipts = [ReceiptUploadsSerializer(
        data={'receipt': request.FILES.get(name)})
                for name in request.FILES
                if name.startswith('receipt')]

    if not all(f.is_valid() for f in receipts):
        return Response(
            status=400,
            data={
                "message": ("Escaped Frontend validation: "
                            "Invalid image file.")})

    return None


def generate_main_message(form):
    """
    Generate the main message for the email, using the form data.
    """
    return (
        f"Name: {form['name']}\n"
        f"Email: {form['email']}\n"
        f"Date of Expense: {form['date']}\n"
        f"Description: {form['description']}\n"
        f"Purpose: {form['purpose']}\n"
        f"Total: {form['total']}\n"
        f"Bank account: {form['iban']}\n"
        f"Account Holder: {form['accountName']}\n\n"
    )


def generate_message_to_submitter(church, submitter):
    """
    Generate the message to the submitter, using the form data.
    """
    return (
        f"Dear {submitter}, \n\n"
        "Thank you for submitting an expense form. "
        "We will process it shortly.\n"
        "If you don't hear from us, or if the reimbursement doesn't arrive "
        "to you within 2 weeks, then please reach out to us at "
        f"{church.finance_email}.\n\n"
        f"{church.finance_contact_name}\n"
        "Finance Team\n"
        f"{church.long_name}\n\n"
    )


def generate_message_to_finance(main_message):
    """
    Generate the message to the finance team, using the form data.
    """
    return (
        "Expense Form Submission\n\n"
        f"{main_message}"
    )


def generate_reply_template(church, submitter, main_message):
    """
    Generate the reply template for the submitter, to be used by the
    finance team, after the reimbursement has been made.
    """
    return (
        f"Dear {submitter},\n\n"
        "Thank you for using your resources for the church. I have "
        "transferred the reimbursement to your account. If you have any "
        "questions, then please reach out to us at "
        f"{church.finance_email}.\n\n"
        f"{church.finance_contact_name}\n"
        "Finance Team\n"
        f"{church.long_name}\n\n"
        "Ps - the submitted data:\n\n"
        f"{main_message}"
    )


def process_file(file, max_size):
    """
    Open the file, if it's an image, resize if necessary and convert it to PDF.
    Return a buffer with the PDF data. Expecting valid image or pdf files.
    """
    # Create a file-like buffer for the form to receive PDF data.
    buffer = BytesIO()

    try:
        # Check if the file is an image or a PDF.
        if file.content_type.startswith('image/'):
            if isinstance(file, InMemoryUploadedFile):
                # It's an image. Open it with PIL and resize it.
                image = PilImage.open(file)

                # Adjust the image data based on the orientation metadata.
                image = ImageOps.exif_transpose(image)

                # Resize the image while keeping the aspect ratio.
                image.thumbnail(max_size)

                # Convert the image to PDF and write it to a buffer.
                image.save(buffer, 'PDF')
                image.close()

        elif file.content_type == 'application/pdf':
            # It's a PDF. Write it directly to the buffer.
            buffer.write(file.read())
        
        else:
            # Even though we don't expect to receive any other file types,
            # we still handle this case in order to future-proof the code.
            return Response(status=406, data={
                            "message": f"Invalid file type for {file.name}"})

    except Exception as e:
        return Response(status=406, data={
                        "message": f"Error processing file {file.name}",
                        "error": str(e)})

    buffer.seek(0)
    return buffer


def generate_form_pdf(form):
    """
    Generate HTML from the form data, convert it to PDF and add it to the
    buffer. Return the buffer.
    """
    if None in form.values():
          return Response(status=500, data={
                          "message": "Empty form data. Cannot generate PDF"})
    # Create a file-like buffer for the form to receive PDF data.
    buffer = BytesIO()
    try:
        html_content = render_to_string('email-template.html', form)
        pisa.CreatePDF(html_content, dest=buffer)
    except Exception as e:
        return Response(status=500, data={"message": "Error generating PDF",
                                          "error": str(e)})

    buffer.seek(0)
    return buffer


def generate_attachment(form):
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

        receipt_buffer = None
        try:
            max_size = (700, 1100)
            receipt_buffer = process_file(receipt_file, max_size)
            if isinstance(receipt_buffer, Response):
                return receipt_buffer

            if receipt_buffer is not None:
                pdf_merge.append(receipt_buffer)

        except Exception as e:
            return Response(status=406, data={"message": "Unfortunately, we \
                                          are unable to process one or more \
                                          image(s) you sent us. Please \
                                          try another format.", "error": e})

        finally:
            if receipt_buffer is not None:
                receipt_buffer.close()

        i += 1

    return pdf_merge