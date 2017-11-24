from __future__ import unicode_literals

from rest_framework import serializers

from members.models.bank_accounts import BankAccount


class BankAccountSerializer(serializers.ModelSerializer):
    holder = serializers.IntegerField(read_only=True)
    currency = serializers.CharField(read_only=True)
    number = serializers.CharField(read_only=True)

    class Meta:
        model = BankAccount
        fields = ('id', 'number', 'balance', 'currency', 'holder')
