from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APITestCase
from claims.serializers import ExpenseSerializer, ReceiptUploadsSerializer

class ExpenseSerializerTestCase(APITestCase):
    def test_valid_data(self):
        data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'church': 'Church Name',
            'purpose': 'Test Purpose',
            'date': '2022-01-01',
            'description': 'Test Description',
            'total': '100',
            'iban': 'GB82 WEST 1234 5698 7654 32',
            'accountName': 'John Doe',
        }
        serializer = ExpenseSerializer(data=data)
        self.assertTrue(serializer.is_valid())
  
    def test_valid_data_with_optional_fields_empty(self):
        data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'church': 'Church Name',
            'purpose': 'Test Purpose',
            'date': '2022-01-01',
            'description': 'Test Description',
            'total': '100',
            'iban': '',
            'accountName': '',
        }
        serializer = ExpenseSerializer(data=data)
        self.assertTrue(serializer.is_valid())
  
    def test_valid_data_with_optional_fields_missing(self):
          data = {
              'name': 'John Doe',
              'email': 'john@example.com',
              'church': 'Church Name',
              'purpose': 'Test Purpose',
              'date': '2022-01-01',
              'description': 'Test Description',
              'total': '100',
          }
          serializer = ExpenseSerializer(data=data)
          self.assertTrue(serializer.is_valid())

    def test_invalid_name(self):
        data = {
            'name': '',
            'email': 'john@example.com',
            'church': 'Church Name',
            'purpose': 'Test Purpose',
            'date': '2022-01-01',
            'description': 'Test Description',
            'total': '100',
            'iban': 'GB82 WEST 1234 5698 7654 32',
            'accountName': 'John Doe',
        }
        serializer = ExpenseSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_invalid_email(self):
        data = {
            'name': 'John Doe',
            'email': 'invalid email',
            'church': 'Church Name',
            'purpose': 'Test Purpose',
            'date': '2022-01-01',
            'description': 'Test Description',
            'total': '100',
            'iban': 'GB82 WEST 1234 5698 7654 32',
            'accountName': 'John Doe',
        }
        serializer = ExpenseSerializer(data=data)
        self.assertFalse(serializer.is_valid())
    
    def test_invalid_date(self):
        data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'church': 'Church Name',
            'purpose': 'Test Purpose',
            'date': 'invalid date',
            'description': 'Test Description',
            'total': '100',
            'iban': 'GB82 WEST 1234 5698 7654 32',
            'accountName': 'John Doe',
        }
        serializer = ExpenseSerializer(data=data)
        self.assertFalse(serializer.is_valid())
  
    def test_invalid_total(self):
        data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'church': 'Church Name',
            'purpose': 'Test Purpose',
            'date': '2022-01-01',
            'description': 'Test Description',
            'total': 'invalid total',
            'iban': 'GB82 WEST 1234 5698 7654 32',
            'accountName': 'John Doe'
        }
        serializer = ExpenseSerializer(data=data)
        self.assertFalse(serializer.is_valid())


class ReceiptUploadsSerializerTestCase(APITestCase):
    def test_no_file(self):
        data = {}
        serializer = ReceiptUploadsSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_valid_jpg_file(self):
        file = SimpleUploadedFile("file.jpg", b"file_content", content_type="image/jpeg")
        data = {'receipt': file}
        serializer = ReceiptUploadsSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_valid_png_file(self):
        file = SimpleUploadedFile("file.png", b"file_content", content_type="image/png")
        data = {'receipt': file}
        serializer = ReceiptUploadsSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_valid_pdf_file(self):
        file = SimpleUploadedFile("file.pdf", b"file_content", content_type="application/pdf")
        data = {'receipt': file}
        serializer = ReceiptUploadsSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_image_file(self):
        file = SimpleUploadedFile("file.gif", b"file_content", content_type="image/gif")
        data = {'receipt': file}
        serializer = ReceiptUploadsSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_invalid_non_image_file(self):
        file = SimpleUploadedFile("file.txt", b"file_content", content_type="text/plain")
        data = {'receipt': file}
        serializer = ReceiptUploadsSerializer(data=data)
        self.assertFalse(serializer.is_valid())