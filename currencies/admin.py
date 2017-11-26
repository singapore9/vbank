from django.contrib import admin

from currencies.models import Currency


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('code', 'country', 'exchange_rate')

    def get_readonly_fields(self, request, obj=None):
        return ['code', ] if obj else []
