from __future__ import absolute_import

from django.contrib.auth import authenticate, get_user_model
from rest_framework.settings import api_settings
from rest_framework import serializers

AuthUserModel = get_user_model()


class LoginSerializer(serializers.Serializer):
    fail_login_message = ''

    def authenticate(self, roles):
        user = authenticate(**self.validated_data)
        if not (user and any([getattr(user, role) for role in roles])):
            raise serializers.ValidationError({
                api_settings.NON_FIELD_ERRORS_KEY: [self.fail_login_message],
            })
        if not user.is_active:
            raise serializers.ValidationError({
                api_settings.NON_FIELD_ERRORS_KEY: ["User inactive or deleted."],
            })
        return user


class UsernameLoginSerializer(LoginSerializer):
    username = serializers.CharField()
    password = serializers.CharField()

    fail_login_message = 'Invalid username or password.'
