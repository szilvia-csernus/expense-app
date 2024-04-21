import unittest
from unittest.mock import patch, MagicMock
from django.test import RequestFactory
from rest_framework.response import Response
from claims.utils import generate_attachment
from pypdf import PdfWriter
from io import BytesIO

class TestGenerateAttachment(unittest.TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()

    @patch('claims.utils.PdfWriter')
    @patch('claims.utils.generate_form_pdf')
    def test_generate_attachment_valid_data(self, mock_generate_form_pdf, mock_PdfWriter):
        # Create a mock file-like object for the receipt
        mock_file = MagicMock()
        mock_file.name = 'test_receipt'

        # Create a form with valid data
        form = {'field1': 'value1', 'field2': 'value2', 'receipt0': mock_file}

        # Mock generate_form_pdf to return a MagicMock object
        mock_generate_form_pdf.return_value = MagicMock()

        # Mock PdfWriter to return MagicMock objects
        mock_PdfWriter.return_value = MagicMock()

        # Generate the attachment
        result = generate_attachment(form)

        # Check that the result is a MagicMock object (which represents a PdfWriter object)
        self.assertIsInstance(result, MagicMock)

    @patch('claims.utils.generate_form_pdf')
    def test_generate_attachment_invalid_data(self, mock_generate_form_pdf):
        # Create a form with invalid data
        form = {'field1': 'value1', 'field2': None, 'receipt0': 'test_receipt'}

        # Mock generate_form_pdf to return a Response object
        mock_generate_form_pdf.return_value = Response(status=500, data={"message": "Error generating PDF"})

        # Generate the attachment
        result = generate_attachment(form)

        # Check that the result is a Response with status code 500
        self.assertIsInstance(result, Response)
        self.assertEqual(result.status_code, 500)
        self.assertEqual(result.data["message"], "Error generating PDF")
