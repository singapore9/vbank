from __future__ import absolute_import

from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.http import Http404
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.settings import api_settings
from rest_framework import serializers

AuthUserModel = get_user_model()


class LoginSerializer(serializers.Serializer):
    fail_login_message = ''

    def authenticate(self, roles):
        user = authenticate(**self.validated_data)
        from_db = AuthUserModel.objects.filter(email=self.validated_data['username'])
        if from_db.exists():
            if from_db.first().is_locked:
                raise serializers.ValidationError({
                    api_settings.NON_FIELD_ERRORS_KEY: ["The user is locked by bank employee."]
                })
            elif not from_db.first().is_active:
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


class ResetPasswordByEmailSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        fields = ['email']
        model = AuthUserModel

    def __init__(self, *args, **kwargs):
        super(ResetPasswordByEmailSerializer, self).__init__(*args, **kwargs)

    def validate_email(self, attrs):
        if not self.Meta.model.objects.filter(email=attrs).exists():
            raise ValidationError("User with such email doesn't exist.")
        return attrs

    def send_reset_password_email(self):
        try:
            user = self.Meta.model.objects.get(email=self.validated_data.get('email'))
        except self.Meta.model.DoesNotExist:
            return

        user.send_reset_password_email()


class PasswordRecoverySrializer(serializers.Serializer):
    new_password1 = serializers.CharField(max_length=128)
    new_password2 = serializers.CharField(max_length=128)
    uid = serializers.CharField(max_length=10)
    token = serializers.CharField(max_length=30)

    def validate_uid(self, value):
        user_model = get_user_model()
        try:
            uid = force_text(urlsafe_base64_decode(value))
        except (TypeError, ValueError):
                raise Http404
        if not user_model.objects.filter(pk=uid).exists():
            raise Http404
        return uid

    def validate(self, attrs):
        new_password1 = attrs.get('new_password1', None)
        new_password2 = attrs.get('new_password2', None)
        uid = attrs.get('uid', None)
        token = attrs.get('token', None)
        if not new_password1 == new_password2:
            raise ValidationError("Passwords don't match.")
        validate_password(new_password1)
        user = get_object_or_404(get_user_model(), pk=uid)
        token_generator = PasswordResetTokenGenerator()
        if not token_generator.check_token(user, token):
            raise Http404
        return attrs

    def save(self, **kwargs):
        data = self.validated_data
        user = get_object_or_404(get_user_model(), pk=data['uid'])
        user.set_password(data['new_password1'])
        user.save()

