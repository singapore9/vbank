from __future__ import unicode_literals

from rest_framework import serializers

from members.models.bank_cards import BankCard


class BankCardSerializer(serializers.ModelSerializer):
    holder = serializers.IntegerField(read_only=True)
    currency_code = serializers.SerializerMethodField()
    number = serializers.CharField(read_only=True)

    class Meta:
        model = BankCard
        fields = ('id', 'holder', 'balance', 'currency_code', 'number')

    def get_currency_code(self, obj):
        return (obj.currency and obj.currency.code) or None

    def get_balance(self, obj):
        return (obj.bank_account and obj.bank_account.balance) or 0