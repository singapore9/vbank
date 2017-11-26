from __future__ import unicode_literals

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from members.models.charges import CardCharge, ExternalCharge


class ChargeBaseSerializer(serializers.ModelSerializer):
    currency_code = serializers.SerializerMethodField()
    value = serializers.FloatField(required=True)

    class Meta:
        fields = ('id', 'sender', 'value', 'currency_code', 'recipient')

    def get_currency_code(self, obj):
        return obj.sender.bank_account.currency.code

    def _validate_charge_value(self, sender, val):
        if sender.balance < val:
            raise ValidationError('Sender bank account has less money than in charge.')

class CardChargeSerializer(ChargeBaseSerializer):
    class Meta(ChargeBaseSerializer.Meta):
        model = CardCharge

    def validate(self, attrs):
        attrs = super(CardChargeSerializer, self).validate(attrs)
        sender = attrs['sender']
        recipient = attrs['recipient']
        value = attrs['value']

        sender_account = sender.bank_account
        recipient_account = recipient.bank_account
        if sender_account.currency != recipient_account.currency:
            raise ValidationError('Currencies of bank accounts does not match.')
        self._validate_charge_value(sender_account, value)

        sender_account.balance -= value
        recipient_account.balance += value
        sender_account.save()
        recipient_account.save()
        return attrs


class ExternalChargeSerializer(ChargeBaseSerializer):
    class Meta(ChargeBaseSerializer.Meta):
        model = ExternalCharge

    def validate(self, attrs):
        attrs = super(ExternalChargeSerializer, self).validate(attrs)
        sender = attrs['sender']
        value = attrs['value']

        sender_account = sender.bank_account
        if sender_account.currency.code != 'BYN':
            raise ValidationError('External charges available only in BYN.')
        self._validate_charge_value(sender_account, value)

        sender_account.balance -= value
        sender_account.save()
        return attrs