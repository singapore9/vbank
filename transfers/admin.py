from django.contrib import admin

from transfers.models import ExternalTransfer, CardTransfer


class BaseTransferAdmin(admin.ModelAdmin):
    list_display = ('sender', 'value', 'recipient', 'created_at')
    readonly_fields = ('sender', 'value', 'recipient', )


@admin.register(ExternalTransfer)
class ExternalTransferAdmin(BaseTransferAdmin):
    pass


@admin.register(CardTransfer)
class CardTransferAdmin(BaseTransferAdmin):
    pass
