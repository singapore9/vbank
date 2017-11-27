from mailing.shortcuts import render_send_email
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from custom_auth.permissions import UserIsAuthenticated
from clients.models.bank_cards import BankAccount, BankCard
from clients.serializers.bank_accounts import BankAccountSerializer
from clients.serializers.bank_cards import BankCardSerializer
from transfers.serializers import InternalTransferSerializer, ExternalTransferSerializer


class OwnerViewSetMixin(mixins.RetrieveModelMixin,
                        mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    permission_classes = [UserIsAuthenticated, ]
    _model = None

    def get_queryset(self):
        client = self.request.user
        return self._model.objects.filter(holder=client)


class BankAccountViewSet(OwnerViewSetMixin):
    serializer_class = BankAccountSerializer
    _model = BankAccount


class BankCardViewSet(OwnerViewSetMixin):
    serializer_class = BankCardSerializer
    _model = BankCard

    @detail_route(methods=['post'], permission_classes=[UserIsAuthenticated, ])
    def transfer(self, request, *args, **kwargs):
        card = self.get_object()
        data = request.data
        data.update([('sender', card.number), ])

        is_external = request.GET.get('external', False)
        transfer_serializer_class = ExternalTransferSerializer if is_external else InternalTransferSerializer

        serializer = transfer_serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        sender_account = serializer.validated_data['sender'].bank_account
        value = serializer.validated_data['value']

        sender_account.balance -= value
        sender_account.save()

        for_send_notification = [sender_account.holder.email, ]

        if not is_external:
            recipient_account = serializer.validated_data['recipient'].bank_account
            if sender_account.currency != recipient_account.currency:
                received_value = value * sender_account.currency.rate.purchase / recipient_account.currency.rate.sale
            else:
                received_value = value
            recipient_account.balance += received_value
            recipient_account.save()
            for_send_notification += [recipient_account.email, ]

        for destination in for_send_notification:
            transfer_type = 'External' if is_external else \
                ('Incoming' if sender_account.holder.email == destination else 'Outcoming')
            context = {
                'transfer_type': transfer_type,
                'sender': sender_account,
                'is_sender': transfer_type != 'Incoming',
                'amount': value,
                'code': sender_account.currency.code,
                'recipient': serializer.validated_data['recipient']
            }
            render_send_email([destination], '/email/transfer_notification/transfer_notification', context, use_base_template=False)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
