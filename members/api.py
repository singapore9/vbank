from rest_framework import viewsets, mixins, status
from rest_framework.decorators import detail_route
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from custom_auth.permissions import UserIsAuthenticated
from members.models import Currency
from members.models.bank_cards import BankAccount, BankCard
from members.serializers.bank_accounts import BankAccountSerializer
from members.serializers.bank_cards import BankCardSerializer
from members.serializers.charges import CardChargeSerializer, ExternalChargeSerializer
from members.serializers.currencies import CurrencySerializer


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
    def charge(self, request, *args, **kwargs):
        card = self.get_object()
        data = request.data
        data.update([('sender', card.number), ])
        serializer = CardChargeSerializer(data=data)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @detail_route(methods=['post'], permission_classes=[UserIsAuthenticated, ], url_path='external-charge')
    def external_charge(self, request, *args, **kwargs):
        card = self.get_object()
        data = request.data
        data.update([('sender', card.number), ])
        serializer = ExternalChargeSerializer(data=data)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CurrenciesViewSet(mixins.RetrieveModelMixin,
                        mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    serializer_class = CurrencySerializer
    permission_classes = [AllowAny, ]
    queryset = Currency.objects.all()
