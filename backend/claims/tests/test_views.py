from django.test import TestCase, RequestFactory
from django.core.mail import EmailMessage
from unittest.mock import patch, MagicMock
from rest_framework.response import Response
from cost_centers.models import Church
from claims.views import send_expense_form
from django.core.files.uploadedfile import SimpleUploadedFile
import logging

class SendExpenseFormTest(TestCase):
    def setUp(self):
        logging.disable(logging.CRITICAL)
        self.factory = RequestFactory()
        self.church = Church.objects.create(short_name='test', finance_email='finance@test.com')
        self.valid_form_data = {
          'church': 'test',
          'name': 'Test User',
          'email': 'test@example.com',
          'purpose': 'Test Purpose',
          'date': '2022-01-01',
          'description': 'Test Description',
          'total': '100.00',
          'iban': 'Test IBAN',
          'accountName': 'Test Account Name',
          'file': SimpleUploadedFile('test_file.pdf', b'file_content', content_type='application/pdf')
        }
  
    def tearDown(self):
      logging.disable(logging.NOTSET)

    @patch('claims.views.validate_form')
    def test_form_validation_failure(self, mock_validate_form):
        mock_validate_form.return_value = Response(status=400)
        request = self.factory.post('/send_expense_form/', {'church': 'test'})
        response = send_expense_form(request)
        self.assertEqual(response.status_code, 400)

    @patch('claims.views.get_object_or_404')
    def test_church_retrieval_failure(self, mock_get_object_or_404):
        mock_get_object_or_404.return_value = None
        request = self.factory.post('/send_expense_form/', {'church': 'test'})
        response = send_expense_form(request)
        self.assertEqual(response.status_code, 400)

    @patch('claims.views.generate_attachment')
    def test_attachment_generation_failure(self, mock_generate_attachment):
        mock_generate_attachment.return_value = Response(status=400)
        request = self.factory.post('/send_expense_form/', {'church': 'test'})
        response = send_expense_form(request)
        self.assertEqual(response.status_code, 400)

    @patch('claims.views.EmailMessage')
    def test_email_sending_failure(self, mock_email_message):
        mock_email = MagicMock(spec=EmailMessage)
        mock_email.send.side_effect = Exception
        mock_email_message.return_value = mock_email
        request = self.factory.post('/send_expense_form/', {'church': 'test'})
        response = send_expense_form(request)
        self.assertEqual(response.status_code, 400)

    @patch('claims.views.EmailMessage')
    def test_successful_email_sending(self, mock_email_message):
        mock_email_message.return_value = MagicMock(success=True)
        request = self.factory.post('/send_expense_form/', self.valid_form_data)
        response = send_expense_form(request)
        self.assertEqual(response.status_code, 200)