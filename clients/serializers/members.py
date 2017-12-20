from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from rest_framework import serializers

from custom_auth.validators import age_validator

UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    is_confirmed = serializers.BooleanField(read_only=True)

    class Meta:
        model = UserModel
        fields = ('first_name', 'middle_name', 'last_name', 'birthday', 'residence_address', 'email', 'username',
                  'is_confirmed', 'password')

    def validate(self, attrs):
        attrs = super(UserSerializer, self).validate(attrs)
        birthday = getattr(attrs, 'birthday', None)
        if birthday:
            age_validator(birthday)
        return attrs

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.role = 1
        user.is_active = False
        user.set_password(validated_data['password'])
        user.save()
        user.send_confirm_account_email()

        return user

    def update(self, instance, validated_data):
        new_email = validated_data.get('email', None)
        old_email = instance.email

        updated = super(UserSerializer, self).update(instance, validated_data)
        if new_email and new_email != old_email:
            updated.is_confirmed = False
            updated.send_confirm_account_email()
            updated.save()

        return updated


class MiniUserSerializer(UserSerializer):

    class Meta(UserSerializer.Meta):
        fields = ('first_name', 'middle_name', 'last_name', 'birthday', 'residence_address', 'email', 'username', )