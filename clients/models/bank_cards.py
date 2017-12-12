from __future__ import unicode_literals

from django.db import models

from clients.models.bank_accounts import BankAccount
from clients.models.members import Member


class BankCard(models.Model):
    number = models.CharField(max_length=30, primary_key=True)
    bank_account = models.ForeignKey(BankAccount)
    holder = models.ForeignKey(Member, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.number:
            self.holder = self.bank_account.holder
            self.number = '3237-{user:0>4}-{account}-{card:0>4}'.format(user=self.holder.pk,
                                                                        account=self.bank_account.number[-4:],
                                                                        card=BankCard.objects.count())
        return super(BankCard, self).save(*args, **kwargs)

    def __str__(self):
        return 'Card {number}'.format(number=self.number)

    def favourite_external_transfers(self):
        from transfers.models import ExternalTransfer

        if not self.pk:
            return ExternalTransfer.objects.none()
        return ExternalTransfer.objects.filter(sender=self.pk).filter(is_favorite=True)
