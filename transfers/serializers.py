from __future__ import unicode_literals

from mailing.shortcuts import render_send_email
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
        return obj.sender.bank_account.currency.code

    def validate(self, attrs):
        sender = attrs['sender']
        val = attrs['value']
        if sender.bank_account.balance < val:
            raise ValidationError('Sender bank account has less money than in transfer.')
        return attrs

    def create(self, validated_data):
        sender_account = validated_data['sender'].bank_account
        value = validated_data['value']

        sender_account.balance -= value
        sender_account.save()

        for_send_notification = [sender_account.holder.email, ]

        try:
            recipient_account = validated_data['recipient'].bank_account
            transfer_type = 'External'
            for_send_notification += [recipient_account.holder.email, ]
        except AttributeError:
            transfer_type = 'Internal'

        for destination in for_send_notification:
            context = {
                'transfer_type': transfer_type,
                'sender': sender_account,
                'is_sender': destination == sender_account.holder.email,
                'amount': value,
                'code': sender_account.currency.code,
                'recipient': validated_data['recipient']
            }
            render_send_email(recipients=[destination, ],
                              template='email/transfer_notification/transfer_notification',
                              data=context,
                              use_base_template=False)

        return super(TransferBaseSerializer, self).create(validated_data)


class InternalTransferSerializer(TransferBaseSerializer):
    class Meta(TransferBaseSerializer.Meta):
        model = InternalTransfer

    def validate(self, attrs):
        attrs = super(InternalTransferSerializer, self).validate(attrs)

        sender = attrs['sender']
        recipient = attrs['recipient']
        if sender.bank_account == recipient.bank_account:
            raise ValidationError('Can not create transfer from bank account to the same one.')
        return attrs

    def create(self, validated_data):
        sender_account = validated_data['sender'].bank_account
        recipient_account = validated_data['recipient'].bank_account
        value = validated_data['value']

        if sender_account.currency != recipient_account.currency:
            received_value = value * sender_account.currency.rate().purchase / recipient_account.currency.rate().sale
        else:
            received_value = value
        recipient_account.balance += received_value
        recipient_account.save()

        return super(InternalTransferSerializer, self).create(validated_data)


class ExternalTransferSerializer(TransferBaseSerializer):
    is_favorite = serializers.BooleanField(default=False)

    class Meta(TransferBaseSerializer.Meta):
        fields = TransferBaseSerializer.Meta.fields + ('is_favorite', )
        model = ExternalTransfer

    def validate(self, attrs):
        attrs = super(ExternalTransferSerializer, self).validate(attrs)

        sender = attrs['sender']
        sender_account = sender.bank_account
        if sender_account.currency.code != 'BYN':
            raise ValidationError('External transfers available only in BYN.')
        return attrs
