from django import forms
from django.core.exceptions import ValidationError


class ExpenseForm(forms.Form):
    name = forms.CharField(max_length=200)
    email = forms.EmailField()
    church = forms.CharField(max_length=200)
    purpose = forms.CharField(max_length=200)
    date = forms.DateField()
    description = forms.CharField(max_length=500)
    total = forms.DecimalField(max_digits=10, decimal_places=2)
    iban = forms.CharField(max_length=34)
    accountName = forms.CharField(max_length=200)
    receipts = forms.ImageField(required=True)


class ImageUploads(forms.Form):
    receipts = forms.ImageField(required=True)

    # This method is used to validate the image file type, overriding the
    # default clean method to include PDF files.
    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            # content_type is the file's MIME type, determined by the browser
            main, sub = image.content_type.split('/')
            if not (main == 'image' and sub in ['jpeg', 'png']) and \
                    not (main == 'application' and sub == 'pdf'):
                raise ValidationError('Unsupported file type. Supported file \
                    types are .jpg, .jpeg, .png, .pdf')
        return image
