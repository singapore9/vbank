from __future__ import unicode_literals

from django.db import models

from members.models.bank_accounts import BankAccount
from members.models.members import Member


class BankCard(models.Model):
    number = models.CharField(max_length=30, primary_key=True)
    bank_account = models.ForeignKey(BankAccount)
    holder = models.ForeignKey(Member, on_delete=models.CASCADE)

    def __str__(self):
        return 'Card {number}'.format(number=self.number)
