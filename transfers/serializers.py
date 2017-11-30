from __future__ import unicode_literals

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from transfers.models import InternalTransfer, ExternalTransfer


class TransferBaseSerializer(serializers.ModelSerializer):
    currency_code = serializers.SerializerMethodField()
    value = serializers.FloatField(required=True)

    class Meta:
        fields = ('id', 'sender', 'value', 'currency_code', 'recipient')
        read_only_fields = ('id', )

    def get_currency_code(self, obj):
        return obj['sender'].bank_account.currency.code

    def validate(self, attrs):
        sender = attrs['sender']
        val = attrs['value']
        if sender.bank_account.balance < val:
            raise ValidationError('Sender bank account has less money than in transfer.')
        return attrs


class InternalTransferSerializer(TransferBaseSerializer):
    class Meta(TransferBaseSerializer.Meta):
        model = InternalTransfer

    def validate(self, attrs):
        attrs = super(ExternalTransferSerializer, self).validate(attrs)

        sender = attrs['sender']
        recipient = attrs['recipient']
        if sender.bank_account == recipient.bank_account:
            raise ValidationError('Can not create transfer from bank account to the same one.')


class ExternalTransferSerializer(TransferBaseSerializer):
    is_favourite = serializers.BooleanField(default=False)

    class Meta(TransferBaseSerializer.Meta):
        fields = TransferBaseSerializer.Meta.fields + ('is_favourite', )
        model = ExternalTransfer

    def validate(self, attrs):
        attrs = super(ExternalTransferSerializer, self).validate(attrs)

        sender = attrs['sender']
        sender_account = sender.bank_account
        if sender_account.currency.code != 'BYN':
            raise ValidationError('External transfers available only in BYN.')
        return attrs
