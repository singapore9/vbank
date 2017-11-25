from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from members.api import BankAccountViewSet, BankCardViewSet, CurrenciesViewSet

router = DefaultRouter()
router.register(r'bank-accounts', BankAccountViewSet, 'bank-accounts')
router.register(r'bank-cards', BankCardViewSet, 'bank-card')
router.register(r'exchange-rates', CurrenciesViewSet, 'exchange-rates')


api_patterns = [
    url(r'', include(router.urls)),
]
