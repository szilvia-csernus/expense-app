from django.urls import path
from .views import ChurchesAndCostPurposes

urlpatterns = [
    path('purposes/', ChurchesAndCostPurposes.as_view()),
]
