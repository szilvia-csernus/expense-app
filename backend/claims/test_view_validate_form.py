from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIRequestFactory, APITestCase
from .utils import validate_form

class ValidateFormTestCase(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

    def test_invalid_form(self):
        request = self.factory.post('/', data={})
        request.data = request.POST
        response = validate_form(request)
        self.assertEqual(response.status_code, 400)
        self.assertIn('Escaped Frontend validation: form.errors', response.data['message'])

    def test_no_files(self):
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
        request = self.factory.post('/', data=data)
        request.data = request.POST
        response = validate_form(request)
        self.assertEqual(response.status_code, 400)
        self.assertIn('Escaped Frontend validation: File upload required.', response.data['message'])

    def test_files_too_large(self):
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
            'receipt1': SimpleUploadedFile("file1.jpg", b"file_content" * 1024 * 1024, content_type="image/jpeg"),
            'receipt2': SimpleUploadedFile("file2.jpg", b"file_content" * 1024 * 1024, content_type="image/jpeg"),
            'receipt3': SimpleUploadedFile("file3.jpg", b"file_content" * 1024 * 1024, content_type="image/jpeg"),
            'receipt4': SimpleUploadedFile("file4.jpg", b"file_content" * 1024 * 1024, content_type="image/jpeg"),
            'receipt5': SimpleUploadedFile("file5.jpg", b"file_content" * 1024 * 1024, content_type="image/jpeg"),
            'receipt6': SimpleUploadedFile("file6.jpg", b"file_content" * 1024 * 1024, content_type="image/jpeg"),
        }
        request = self.factory.post('/', data=data)
        request.data = request.POST
        response = validate_form(request)
        self.assertEqual(response.status_code, 400)
        self.assertIn('Escaped Frontend validation: The total size of all files exceeds the limit.', response.data['message'])

    def test_invalid_file(self):
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
            'receipt': SimpleUploadedFile("file.txt", b"file_content", content_type="text/plain"),
        }
        request = self.factory.post('/', data=data)
        request.data = request.POST
        response = validate_form(request)
        self.assertEqual(response.status_code, 400)
        self.assertIn('Escaped Frontend validation: Invalid image file.', response.data['message'])

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
            'receipt': SimpleUploadedFile("file.jpg", b"file_content", content_type="image/jpeg"),
        }
        request = self.factory.post('/', data=data)
        request.data = request.POST
        response = validate_form(request)
        self.assertIsNone(response)