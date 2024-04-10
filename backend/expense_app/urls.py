from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from .views import home


urlpatterns = [
    path('', home),
    path('admin/', admin.site.urls),
    path('claims/', include('claims.urls')),
    path('churches/', include('cost_centers.urls')),
]
