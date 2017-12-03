from datetime import datetime

from django.core.exceptions import FieldDoesNotExist
from rest_framework import viewsets, mixins

from custom_auth.permissions import UserIsAuthenticated
from transfers.models import InternalTransfer, ExternalTransfer
from transfers.serializers import InternalTransferSerializer, ExternalTransferSerializer


class BaseTransfersViewSet(mixins.RetrieveModelMixin,
                           mixins.ListModelMixin,
                           viewsets.GenericViewSet):
    permission_classes = [UserIsAuthenticated, ]
    _model = None

    def get_queryset(self):
        queryset = self._model.objects.all()

        _from = self.request.query_params.get('from', None)
        _to = self.request.query_params.get('to', None)

        if _from:
            queryset = queryset.filter(created_at__gte=datetime.strptime(_from, '%Y-%m-%dT%H:%M:%S'))
        if _to:
            queryset = queryset.filter(created_at__lte=datetime.strptime(_to, '%Y-%m-%dT%H:%M:%S'))

        return queryset


class InternalTransfersViewSet(BaseTransfersViewSet):
    serializer_class = InternalTransferSerializer
    _model = InternalTransfer

    def get_queryset(self):
        queryset = super(InternalTransfersViewSet, self).get_queryset()
        client = self.request.user

        incoming = str(self.request.query_params.get('incoming', False))
        if incoming.lower() == 'false':
            queryset = queryset.filter(sender__holder=client)
        else:
            try:
                queryset = queryset.filter(recipient__holder=client)
            except FieldDoesNotExist:
                pass
        return queryset


class ExternalTransfersViewSet(BaseTransfersViewSet):
    serializer_class = ExternalTransferSerializer
    _model = ExternalTransfer

    def get_queryset(self):
        queryset = super(ExternalTransfersViewSet, self).get_queryset()
        client = self.request.user

        queryset = queryset.filter(sender__holder=client)
        favorite = str(self.request.query_params.get('favorite', False))
        if favorite.lower() == 'true':
            queryset = queryset.filter(is_favorite=True)
        return queryset
