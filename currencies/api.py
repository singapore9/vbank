from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny

from currencies.models import Currency
from currencies.serializers import CurrencySerializer


class CurrenciesViewSet(mixins.RetrieveModelMixin,
                        mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    serializer_class = CurrencySerializer
    permission_classes = [AllowAny, ]
    queryset = Currency.objects.all()
