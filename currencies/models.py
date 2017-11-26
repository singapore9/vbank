from __future__ import unicode_literals

from django.db import models


class Currency(models.Model):
    code = models.CharField(max_length=3, primary_key=True)
    country = models.CharField(max_length=50)
    sale_rate = models.FloatField(help_text='against the BYN')
    purchase_rate = models.FloatField(help_text='against the BYN')

    class Meta:
        verbose_name_plural = "currencies"

    def __str__(self):
        return '{code} ({country})'.format(code=self.code, country=self.country)
