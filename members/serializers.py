from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = '__all__'


class MiniUserSerializer(UserSerializer):

    class Meta(UserSerializer.Meta):
        fields = ('first_name', 'middle_name', 'last_name', 'birthday', 'residence_address', 'email', 'username', )