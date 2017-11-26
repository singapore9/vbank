from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

from members.models import BankCard


class ChargeBase(models.Model):
    value = models.FloatField()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True


class CardCharge(ChargeBase):
    sender = models.ForeignKey(BankCard, related_name='outgoing_charges')
    recipient = models.ForeignKey(BankCard, related_name='incoming_charges')


class ExternalCharge(ChargeBase):
    sender = models.ForeignKey(BankCard, related_name='external_charges')
    recipient = models.CharField(max_length=30)
