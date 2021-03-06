from __future__ import unicode_literals

from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone


class Currency(models.Model):
    code = models.CharField(max_length=3, primary_key=True)
    country = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "currencies"

    def __str__(self):
        return '{code} ({country})'.format(code=self.code, country=self.country)

    def rate(self):
        return self.rates.filter(date__lte=timezone.now()).first()


class CurrencyRate(models.Model):
    date = models.DateField()
    currency = models.ForeignKey(Currency, related_name='rates')
    sale = models.FloatField(help_text='against the BYN', validators=[MinValueValidator(0)])
    purchase = models.FloatField(help_text='against the BYN', validators=[MinValueValidator(0)])

    class Meta:
        ordering = ['-date']
