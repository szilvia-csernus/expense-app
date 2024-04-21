import unittest
from django.test import RequestFactory
from rest_framework.response import Response
from io import BytesIO
from unittest.mock import patch
from claims.utils import generate_form_pdf

class TestGenerateFormPdf(unittest.TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()

    def test_generate_form_pdf_valid_data(self):
        # Create a form with valid data
        form = {'field1': 'value1', 'field2': 'value2'}

        # Generate the PDF
        result = generate_form_pdf(form)

        # Check that the result is a BytesIO object
        self.assertIsInstance(result, BytesIO)

    def test_generate_form_pdf_invalid_data(self):
        # Create a form with invalid data
        form = {'field1': 'value1', 'field2': None}

        # Generate the PDF
        result = generate_form_pdf(form)

        # Check that the result is a Response with status code 500
        self.assertIsInstance(result, Response)
        self.assertEqual(result.status_code, 500)
        self.assertEqual(result.data["message"], "Empty form data. Cannot generate PDF")

    def test_generate_form_pdf_exception_raised(self):
        # Create a form with valid data
        form = {'field1': 'value1', 'field2': 'value2'}

        # Mock pisa.CreatePDF to raise an exception
        with patch('xhtml2pdf.pisa.CreatePDF', side_effect=Exception('Test exception')):
            result = generate_form_pdf(form)

        # Check that the result is a Response with status code 500
        self.assertIsInstance(result, Response)
        self.assertEqual(result.status_code, 500)
        self.assertEqual(result.data["message"], "Error generating PDF")
        self.assertEqual(result.data["error"], "Test exception")