from django.contrib import admin

from .models import Contract


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'contact_person',
        'phone',
        'company_brand',
        'project_type',
        'expected_quantity',
        'delivery_city',
        'budget_range',
        'requirement_description',
    )
    search_fields = ('contact_person', 'phone', 'company_brand', 'delivery_city')
    list_filter = ('project_type', 'delivery_city', 'budget_range')
    ordering = ('-id',)
    list_per_page = 20
