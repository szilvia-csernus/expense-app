from django.contrib import admin

from .models import Church, CostPurpose


class CostPurposeInline(admin.TabularInline):
    model = CostPurpose
    extra = 1
    fields = ['name', 'cost_code']


class ChurchAdmin(admin.ModelAdmin):
    inlines = [CostPurposeInline]
    list_display = ('name', 'logo')


admin.site.register(Church, ChurchAdmin)
