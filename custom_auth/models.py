from __future__ import absolute_import

from mailing.shortcuts import render_send_email

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.contrib.auth.tokens import default_token_generator
from django.core import validators
from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import ugettext_lazy as _


class PasswordTokenMixin(object):
    def _get_token_url(self, token_generator, reset_name):
        uid = urlsafe_base64_encode(force_bytes(self.pk))
        token = token_generator.make_token(self)
        return '/{0}/{1}/{2}'.format(reset_name, uid, token)


class SendMessageMixin(object):
    default_template_name = None
    default_email_address = None
    default_phone = None
    default_sms_sender = None

    def send_email(self, template_name=None, instance_name=None, email=None,
                   extra_context=None, **kwargs):
        template_name = template_name or self.default_template_name
        email = email or self.default_email_address or getattr(self, 'email', None)
        if not (template_name and email):
            return

        class_name = instance_name or self.__class__.__name__.lower()
        context = dict([(class_name, self)])
        context.update(extra_context or {})

        render_send_email([email], template_name, context, use_base_template=False, **kwargs)


class ResetPasswordMixin(PasswordTokenMixin, SendMessageMixin, models.Model):
    reset_password_email_template = 'email/reset_password/reset_password'
    reset_name = 'reset'
    reset_password_token_generator = default_token_generator

    class Meta:
        abstract = True

    def get_password_reset_url(self):
        return self._get_token_url(self.reset_password_token_generator, self.reset_name)

    def send_reset_password_email(self):
        self.send_email(self.reset_password_email_template, 'user')


class ConfirmAccountManagerMixin(object):
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_confirmed', True)
        username = email
        return super(ConfirmAccountManagerMixin, self).create_superuser(username, email, password, **extra_fields)


class ConfirmAccountMixin(SendMessageMixin, models.Model):
    confirm_account_email_template = 'email/confirm_account/confirm_account'
    confirm_account_token_generator = default_token_generator

    is_confirmed = models.BooleanField(_('confirmed'), default=False,
        help_text=_('Designates whether this user confirm his account.'))

    class Meta:
        abstract = True

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        is_new = not self.pk

        super(ConfirmAccountMixin, self).save(force_insert, force_update, using, update_fields)

        if is_new and not self.is_confirmed:
            self.send_confirm_account_email()

    def get_confirm_account_url(self):
        uid = urlsafe_base64_encode(force_bytes(self.pk))
        token = self.confirm_account_token_generator.make_token(self)
        return reverse('account_confirm', kwargs={'uidb64': uid, 'token': token})

    def send_confirm_account_email(self):
        self.send_email(self.confirm_account_email_template, 'user')


class ApplicationUserManager(ConfirmAccountManagerMixin, UserManager):
    pass


class ApplicationUser(AbstractBaseUser, PermissionsMixin, ResetPasswordMixin, ConfirmAccountMixin):

    username = models.CharField(
        _('username'),
        max_length=256,
        unique=True,
        help_text=_('Required. 256 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[
            validators.RegexValidator(
                r'^[\w.@+-]+$',
                _('Enter a valid username. This value may contain only '
                  'letters, numbers ' 'and @/./+/-/_ characters.')
            ),
        ],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    middle_name = models.CharField(_('middle name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    email = models.EmailField(_('email address'), unique=True, blank=False, null=False)
    birthday = models.DateField(null=True)
    residence_address = models.CharField(_('residence address'), max_length=255, blank=True)

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        abstract = True

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    @property
    def full_name(self):
        return self.get_full_name()

    def get_short_name(self):
        """
        Returns the short name for the user.
        """
        return self.first_name
