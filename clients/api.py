from rest_framework import viewsets, mixins, status
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from custom_auth.permissions import UserIsAuthenticated
from clients.models.bank_cards import BankAccount, BankCard
from clients.serializers.bank_accounts import BankAccountSerializer
from clients.serializers.bank_cards import BankCardSerializer
from transfers.serializers import CardTransferSerializer, ExternalTransferSerializer


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
        transfer_serializer_class = ExternalTransferSerializer if is_external else CardTransferSerializer

        serializer = transfer_serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
