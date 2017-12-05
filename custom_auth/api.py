from __future__ import absolute_import

from django.db.transaction import atomic
from rest_framework import decorators, mixins, permissions, status, viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from django.contrib.auth import get_user_model

from clients.serializers.members import UserSerializer, MiniUserSerializer

from .permissions import IsSelfOrReadOnly, POSTOnlyIfAnonymous, UserIsAuthenticated
from .serializers import UsernameLoginSerializer, ChangePasswordSerializer


class RetrieveSelfMixin(object):
    def get_object(self):
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        if self.kwargs[lookup_url_kwarg] == 'me':
            obj = self.request.user
            self.check_object_permissions(self.request, obj)
            return obj

        return super(RetrieveSelfMixin, self).get_object()


class UserViewSet(RetrieveSelfMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.CreateModelMixin,
                  viewsets.GenericViewSet):
    serializer_class = UserSerializer
    queryset = get_user_model().objects
    permission_classes = [IsSelfOrReadOnly, POSTOnlyIfAnonymous]

    def update(self, request, *args, **kwargs):
        kwargs.update({'partial': True})
        return super(UserViewSet, self).update(request, *args, **kwargs)

    def get_serializer_class(self):
        return self.serializer_class

    def create(self, request, *args, **kwargs):
        response = super(UserViewSet, self).create(request, *args, **kwargs)
        response.data = None
        return response

    @detail_route(methods=['put', 'patch'], permission_classes=[UserIsAuthenticated, ], url_path='change-password')
    def change_password(self, request, *args, **kwargs):
        object = self.get_object()
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            old_password = serializer.data.get("old_password")
            if not object.check_password(old_password):
                return Response({"old_password": ["Wrong old password."]},
                                status=status.HTTP_400_BAD_REQUEST)
            object.set_password(serializer.data.get("new_password"))
            object.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserAuthViewSet(viewsets.ViewSet):
    NEW_TOKEN_HEADER = 'X-Token'

    login_serializer_class = UsernameLoginSerializer

    @atomic
    def _basic_login(self, roles):
        serializer = self.get_login_serializer()
        serializer.is_valid(raise_exception=True)
        self.user = serializer.authenticate(roles)
        # self._remove_tokens(self.user)
        return Response(status=status.HTTP_201_CREATED,
                        headers=self.get_success_headers(),
                        data=MiniUserSerializer(instance=self.user).data)

    @staticmethod
    def _remove_tokens(user, token=None):
        if user.is_client:
            tokens_for_delete = user.user_auth_tokens.all()
        else:
            tokens_for_delete = user.user_auth_tokens.filter(key=token)
        tokens_for_delete.delete()

    @decorators.list_route(methods=['post'], permission_classes=[permissions.AllowAny], url_path='login-client')
    def login_client(self, request, roles=['is_client']):
        return self._basic_login(roles)

    def get_login_serializer(self, **kwargs):
        return self.login_serializer_class(data=self.request.data, **kwargs)

    def get_success_headers(self):
        return {self.NEW_TOKEN_HEADER: self.user.user_auth_tokens.create()}

    @decorators.list_route(methods=['delete'], permission_classes=[permissions.IsAuthenticated], url_path='logout')
    def logout(self, request):
        auth_token = request._request.META.get('HTTP_AUTHORIZATION', '').split(' ')[-1]

        self._remove_tokens(request.user, auth_token)

        return Response(None, status=status.HTTP_204_NO_CONTENT)
