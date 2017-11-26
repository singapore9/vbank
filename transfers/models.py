from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

from clients.models.bank_cards import BankCard


class TransferBase(models.Model):
    value = models.FloatField()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True


class InternalTransfer(TransferBase):
    sender = models.ForeignKey(BankCard, related_name='outgoing_transfers')
    recipient = models.ForeignKey(BankCard, related_name='incoming_transfers')


class ExternalTransfer(TransferBase):
    sender = models.ForeignKey(BankCard, related_name='external_transfers')
    is_favourite = models.BooleanField(default=False)
    recipient = models.CharField(max_length=30)
