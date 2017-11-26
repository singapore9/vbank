from django.contrib import admin

from transfers.models import ExternalTransfer, InternalTransfer


class BaseTransferAdmin(admin.ModelAdmin):
    list_display = ('sender', 'value', 'recipient', 'created_at')
    readonly_fields = ('sender', 'value', 'recipient', )


@admin.register(ExternalTransfer)
class ExternalTransferAdmin(BaseTransferAdmin):
    pass


@admin.register(InternalTransfer)
class InternalTransferAdmin(BaseTransferAdmin):
    pass
