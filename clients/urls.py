from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from clients.api import BankAccountViewSet, BankCardViewSet

router = DefaultRouter()
router.register(r'bank-accounts', BankAccountViewSet, 'bank-accounts')
router.register(r'bank-cards', BankCardViewSet, 'bank-card')


api_patterns = [
    url(r'', include(router.urls)),
]
