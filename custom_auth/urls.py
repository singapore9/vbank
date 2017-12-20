from __future__ import absolute_import

from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter

from .models import ApplicationUser
from .views import account_confirm
from .api import UserViewSet, UserAuthViewSet


urlpatterns = \
    [
        url(r'^reset-password/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/?$',
            auth_views.password_reset_confirm, {'template_name': 'custom_auth/password_reset_form.html',
                                                'token_generator': ApplicationUser.reset_password_token_generator},
            name='password_reset_confirm'),
        url(r'^reset-password/done/?$', auth_views.password_reset_complete,
            {'template_name': 'custom_auth/password_reset.html'},
            name='password_reset_complete'),
        url(r'^confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/?$',
            account_confirm, {'token_generator': ApplicationUser.confirm_account_token_generator},
            name='account_confirm'),

    ]


router = DefaultRouter()
router.register(r'auth', UserAuthViewSet, 'auth')
router.register(r'users', UserViewSet)

api_patterns = [
    url(r'', include(router.urls)),
]
