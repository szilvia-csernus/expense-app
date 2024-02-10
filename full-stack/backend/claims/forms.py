from django import forms
from django.core.exceptions import ValidationError


class ExpenseForm(forms.Form):
    name = forms.CharField(max_length=200)
    email = forms.EmailField()
    church = forms.CharField(max_length=200)
    purpose = forms.CharField(max_length=210)
    date = forms.DateField()
    description = forms.CharField(max_length=200)
    total = forms.DecimalField(max_digits=10, decimal_places=2)
    iban = forms.CharField(max_length=34)
    accountName = forms.CharField(max_length=200, required=False)


class ReceiptUploads(forms.Form):
    receipt = forms.FileField(required=False)

    # This method is used to validate uploaded receipts' file types
    def clean_receipt(self):
        receipt = self.cleaned_data.get('receipt')
        if receipt:
            # content_type is the file's MIME type, determined by the browser
            main, sub = receipt.content_type.split('/')
            if not (main == 'image' and sub in ['jpeg', 'png']) and \
                    not (main == 'application' and sub == 'pdf'):
                raise ValidationError('Unsupported file type. Supported file \
                    types are .jpg, .jpeg, .png, .pdf')
        return receipt
