from django.urls import path
from .views import ChurchDetails, ChurchList

urlpatterns = [
    path('details/', ChurchDetails.as_view()),
    path('names/', ChurchList.as_view()),
]
