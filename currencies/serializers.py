from __future__ import unicode_literals

from rest_framework import serializers

from currencies.models import Currency


class CurrencySerializer(serializers.ModelSerializer):

    class Meta:
        model = Currency
        fields = ('code', 'country', 'exchange_rate')
