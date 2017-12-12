from __future__ import unicode_literals

from django.db import models

from currencies.models import Currency
from clients.models.members import Member


class BankAccount(models.Model):
    number = models.CharField(max_length=63, primary_key=True)
    balance = models.FloatField()
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT)
    holder = models.ForeignKey(Member, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.number:
            self.number = 'BYAKVB{user:0>13}{currency:0>3}{account:0>4}'.format(user=self.holder.pk,
                                                                                currency=self.currency.code,
                                                                                account=BankAccount.objects.count())
        return super(BankAccount, self).save(*args, **kwargs)

    def __str__(self):
        return '{number} {user}'.format(number=self.number, user=self.holder)
