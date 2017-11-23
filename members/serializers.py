from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from rest_framework import serializers

UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    is_confirmed = serializers.BooleanField(read_only=True)

    class Meta:
        model = UserModel
        fields = ('first_name', 'middle_name', 'last_name', 'birthday', 'residence_address', 'email', 'username',
                  'is_confirmed', 'password')

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.role = 1
        user.is_active = False
        user.set_password(validated_data['password'])
        user.save()
        user.send_confirm_account_email()

        return user


class MiniUserSerializer(UserSerializer):

    class Meta(UserSerializer.Meta):
        fields = ('first_name', 'middle_name', 'last_name', 'birthday', 'residence_address', 'email', 'username', )