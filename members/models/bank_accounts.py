from __future__ import unicode_literals

from django.db import models

from members.models.currencies import Currency
from members.models.members import Member


class BankAccount(models.Model):
    number = models.CharField(max_length=63)
    balance = models.FloatField()
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT)
    holder = models.ForeignKey(Member, on_delete=models.CASCADE)

    def __str__(self):
        return '{currency_code} {number}'.format(currency_code=(self.currency and self.currency.code) or '---',
                                                 number=self.number)
