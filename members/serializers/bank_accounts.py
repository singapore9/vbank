from __future__ import unicode_literals

from rest_framework import serializers

from members.models.bank_accounts import BankAccount


class BankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccount
        fields = ('id', 'number', 'balance', 'currency', 'holder')
