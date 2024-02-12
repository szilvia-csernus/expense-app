from django.contrib import admin

from .models import Church, CostPurpose


class CostPurposeInline(admin.TabularInline):
    model = CostPurpose
    extra = 1
    fields = ['name', 'cost_code']


class ChurchAdmin(admin.ModelAdmin):
    inlines = [CostPurposeInline]
    list_display = ('short_name', 'long_name', 'logo', 'claims_counter',
                    'finance_contact_name', 'finance_email')


admin.site.register(Church, ChurchAdmin)
