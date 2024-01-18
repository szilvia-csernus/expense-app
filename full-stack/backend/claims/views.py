from django.core.mail import send_mail
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['POST'])
def send_expense_form(request):
    send_mail(
        'Expense Form',
        'Here is the message.',
        settings.DEFAULT_FROM_EMAIL,
        ['csernus.szilvi@gmail.com']
    )
    return Response(status=200, data={"message": "Email sent."})
