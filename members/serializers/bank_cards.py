from __future__ import unicode_literals

from rest_framework import serializers

from members.models.bank_cards import BankCard


class BankCardSerializer(serializers.ModelSerializer):
    currency_code = serializers.SerializerMethodField()
    balance = serializers.SerializerMethodField()

    class Meta:
        model = BankCard
        fields = ('holder', 'balance', 'currency_code', 'number')

    def get_currency_code(self, obj):
        return obj.bank_account.currency.code

    def get_balance(self, obj):
        return obj.bank_account.balance
