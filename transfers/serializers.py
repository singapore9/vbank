from __future__ import unicode_literals

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from transfers.models import InternalTransfer, ExternalTransfer


class TransferBaseSerializer(serializers.ModelSerializer):
    currency_code = serializers.SerializerMethodField()
    value = serializers.FloatField(required=True)

    class Meta:
        fields = ('id', 'sender', 'value', 'currency_code', 'recipient')

    def get_currency_code(self, obj):
        return obj.sender.bank_account.currency.code

    def _validate_transfer_value(self, sender, val):
        if sender.balance < val:
            raise ValidationError('Sender bank account has less money than in transfer.')


class InternalTransferSerializer(TransferBaseSerializer):
    class Meta(TransferBaseSerializer.Meta):
        model = InternalTransfer

    def validate(self, attrs):
        attrs = super(InternalTransferSerializer, self).validate(attrs)
        sender = attrs['sender']
        recipient = attrs['recipient']
        value = attrs['value']

        sender_account = sender.bank_account
        recipient_account = recipient.bank_account
        self._validate_transfer_value(sender_account, value)
        if sender_account.currency != recipient_account.currency:
            received_value = value * sender_account.currency.purchase_rate / recipient_account.currency.sale_rate
        else:
            received_value = value

        sender_account.balance -= value
        recipient_account.balance += received_value
        sender_account.save()
        recipient_account.save()
        return attrs


class ExternalTransferSerializer(TransferBaseSerializer):
    class Meta(TransferBaseSerializer.Meta):
        model = ExternalTransfer

    def validate(self, attrs):
        attrs = super(ExternalTransferSerializer, self).validate(attrs)
        sender = attrs['sender']
        value = attrs['value']

        sender_account = sender.bank_account
        if sender_account.currency.code != 'BYN':
            raise ValidationError('External transfers available only in BYN.')
        self._validate_transfer_value(sender_account, value)

        sender_account.balance -= value
        sender_account.save()
        return attrs