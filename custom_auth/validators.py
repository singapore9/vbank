import re
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils.datetime_safe import date
from django.utils.deconstruct import deconstructible
from django.utils.translation import ugettext_lazy as _


@deconstructible
class NameValidator(RegexValidator):
    def __init__(self, field_name='Name'):
        self.message = '%s must contain only letters, spaces and _ characters. First letter must be capital.' % (field_name, )
        super(NameValidator, self).__init__(regex=r'^[A-Z][a-zA-Z\-\s]*$')


def not_future_validator(value):
    today = date.today()
    if value >= today:
        raise ValidationError('Date must be from past, not today or future.')


def age_validator(value):
    MIN_AGE = 14
    today = date.today()
    if (value - today).days < MIN_AGE * 365:
        raise ValidationError('Account holder must be at least %d years old' % MIN_AGE)


class HasLowerCasePasswordValidator(object):
    def validate(self, password, user=None):
        regexp = re.compile(r'[a-z]')
        if regexp.search(password):
            raise ValidationError(
                _("This password must contain at least 1 lowercase letter."),
                code='password_without_lowercase_letters',
            )

    def get_help_text(self):
        return _("Your password can't be created without lowercase letters.")


class HasUpperCasePasswordValidator(object):
    def validate(self, password, user=None):
        regexp = re.compile(r'[A-Z]')
        if regexp.search(password):
            raise ValidationError(
                _("This password must contain at least 1 uppercase letter."),
                code='password_without_uppercase_letters',
            )

    def get_help_text(self):
        return _("Your password can't be created without uppercase letters.")


class HasDigitPasswordValidator(object):
    def validate(self, password, user=None):
        regexp = re.compile(r'[0-9]')
        if regexp.search(password):
            raise ValidationError(
                _("Password must contain at least 1 digit."),
                code='password_without_digits',
            )

    def get_help_text(self):
        return _("Your password can't be created without numbers.")