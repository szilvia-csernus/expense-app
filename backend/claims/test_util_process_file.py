import unittest
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
from io import BytesIO
from .utils import process_file

class TestProcessFile(unittest.TestCase):
    def test_process_image_file(self):
        # Create a simple image file
        image = Image.new('RGB', (60, 30), color = 'red')
        img_byte_arr = BytesIO()
        image.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        file = SimpleUploadedFile("file.jpg", img_byte_arr, content_type='image/jpeg')

        # Process the image file
        result = process_file(file, (50, 50))

        # Check that the result is a BytesIO object
        self.assertIsInstance(result, BytesIO)

    def test_process_pdf_file(self):
        # Create a simple PDF file
        file_content = b"%PDF-1.4\n%PDF\n"
        file = SimpleUploadedFile("file.pdf", file_content, content_type='application/pdf')

        # Process the PDF file
        result = process_file(file, (50, 50))

        # Check that the result is a BytesIO object
        self.assertIsInstance(result, BytesIO)

    def test_process_invalid_file(self):
        # Create an invalid file
        file_content = b"invalid content"
        file = SimpleUploadedFile("file.txt", file_content, content_type='text/plain')

        # Process the invalid file
        result = process_file(file, (50, 50))

        # Check that the result is a Response with status code 406
        self.assertEqual(result.status_code, 406)
        self.assertEqual(result.data["message"], "Invalid file type for file.txt")