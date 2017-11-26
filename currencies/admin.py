from django.contrib import admin

from currencies.models import Currency, CurrencyRate


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('code', 'country')

    def get_readonly_fields(self, request, obj=None):
        return ['code', ] if obj else []


@admin.register(CurrencyRate)
class CurrencyRateAdmin(admin.ModelAdmin):
    list_display = ('currency', 'date', 'purchase', 'sale')
