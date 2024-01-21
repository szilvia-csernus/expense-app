from django.contrib import admin
from .models import ClaimsCounter


class ClaimsCounterAdmin(admin.ModelAdmin):
    name = 'Claims Counter'


admin.site.register(ClaimsCounter, ClaimsCounterAdmin)
