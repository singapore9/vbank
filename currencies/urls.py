from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from currencies.api import CurrenciesViewSet

router = DefaultRouter()
router.register(r'exchange-rates', CurrenciesViewSet, 'exchange-rates')


api_patterns = [
    url(r'', include(router.urls)),
]
