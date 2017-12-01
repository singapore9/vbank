from __future__ import unicode_literals

from rest_framework import serializers

from currencies.models import Currency


class CurrencySerializer(serializers.ModelSerializer):
    sale_rate = serializers.SerializerMethodField()
    purchase_rate = serializers.SerializerMethodField()

    class Meta:
        model = Currency
        fields = ('code', 'country', 'sale_rate', 'purchase_rate')

    def get_sale_rate(self, obj):
        return obj.rates.first().sale

    def get_purchase_rate(self, obj):
        return obj.rates.first().purchase
