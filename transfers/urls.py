from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from transfers.api import ExternalTransfersViewSet, InternalTransfersViewSet

router = DefaultRouter()
router.register(r'transfers/internal', InternalTransfersViewSet, 'internal-transfers')
router.register(r'transfers/external', ExternalTransfersViewSet, 'external-transfers')

api_patterns = [
    url(r'', include(router.urls)),
]
