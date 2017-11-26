from __future__ import unicode_literals

from django.db import models

from clients.models.bank_accounts import BankAccount
from clients.models.members import Member


class BankCard(models.Model):
    number = models.CharField(max_length=30, primary_key=True)
    bank_account = models.ForeignKey(BankAccount)
    holder = models.ForeignKey(Member, on_delete=models.CASCADE)

    def __str__(self):
        return 'Card {number}'.format(number=self.number)

    def favourite_external_transfers(self):
        from transfers.models import ExternalTransfer

        if not self.pk:
            return ExternalTransfer.objects.none()
        return ExternalTransfer.objects.filter(sender=self.pk).filter(is_favourite=True)

    def favourite_internal_transfers(self):
        from transfers.models import InternalTransfer

        if not self.pk:
            return InternalTransfer.objects.none()
        return InternalTransfer.objects.filter(sender=self.pk).filter(is_favourite=True)
