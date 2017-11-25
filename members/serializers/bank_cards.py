from __future__ import unicode_literals

from rest_framework import serializers

from members.models.bank_cards import BankCard


class BankCardSerializer(serializers.ModelSerializer):
    currency_code = serializers.SerializerMethodField()
    balance = serializers.SerializerMethodField()

    class Meta:
        model = BankCard
        fields = ('id', 'holder', 'balance', 'currency_code', 'number')

    def get_currency_code(self, obj):
        return (obj.bank_account and obj.bank_account.currency and obj.bank_account.currency.code) or None

    def get_balance(self, obj):
        return (obj.bank_account and obj.bank_account.balance) or 0
