from __future__ import absolute_import

from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework.settings import api_settings
from rest_framework import serializers

AuthUserModel = get_user_model()


class LoginSerializer(serializers.Serializer):
    fail_login_message = ''

    def authenticate(self, roles):
        user = authenticate(**self.validated_data)
        from_db = AuthUserModel.objects.filter(email=self.validated_data['username'])
        if from_db.exists() and not from_db.first().is_active:
            raise serializers.ValidationError({
                api_settings.NON_FIELD_ERRORS_KEY: ["The user is not confirmed by bank employee."]
            })
        if not (user and any([getattr(user, role) for role in roles])):
            raise serializers.ValidationError({
                api_settings.NON_FIELD_ERRORS_KEY: [self.fail_login_message],
            })
        if not user.is_confirmed:
            raise serializers.ValidationError({
                "email": ["The email is not confirmed."],
            })
        return user


class UsernameLoginSerializer(LoginSerializer):
    username = serializers.CharField()
    password = serializers.CharField()

    fail_login_message = 'Invalid username or password.'


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        validate_password(value)
        return value
