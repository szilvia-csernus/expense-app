from rest_framework import serializers


class ExpenseSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
    email = serializers.EmailField()
    church = serializers.CharField(max_length=200)
    purpose = serializers.CharField(max_length=210)
    date = serializers.DateField()
    description = serializers.CharField(max_length=200)
    total = serializers.CharField(max_length=10)
    iban = serializers.CharField(max_length=34, required=False)
    accountName = serializers.CharField(max_length=200, required=False)


class ReceiptUploadsSerializer(serializers.Serializer):
    receipt = serializers.FileField(required=False)

    def validate_receipt(self, value):
        if value:
            # content_type is the file's MIME type, determined by the browser
            main, sub = value.content_type.split('/')
            if not (main == 'image' and sub in ['jpeg', 'png']) and \
                    not (main == 'application' and sub == 'pdf'):
                raise serializers.ValidationError('Unsupported file type. \
                    Supported file types are .jpg, .jpeg, .png, .pdf')
        return value
