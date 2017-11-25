from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny

from custom_auth.permissions import UserIsAuthenticated
from members.models import Currency
from members.models.bank_cards import BankAccount, BankCard
from members.serializers.bank_accounts import BankAccountSerializer
from members.serializers.bank_cards import BankCardSerializer
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


class CurrenciesViewSet(mixins.RetrieveModelMixin,
                        mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    serializer_class = CurrencySerializer
    permission_classes = [AllowAny, ]
    queryset = Currency.objects.all()
