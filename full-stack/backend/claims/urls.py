from django.urls import path
from .views import send_expense_form

urlpatterns = [
    path('send_expense_form/', send_expense_form),
]
