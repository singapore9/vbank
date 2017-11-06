from __future__ import unicode_literals

from django.db import models

from custom_auth.models import ApplicationUserManager, ApplicationUser


class MemberManager(ApplicationUserManager):
    def get_queryset(self):
        return super(MemberManager, self).get_queryset()


class ClientsManager(ApplicationUserManager):
    def get_queryset(self):
        return super(ClientsManager, self).get_queryset().filter(role=Member.CLIENT)


class ManagersManager(ApplicationUserManager):
    def get_queryset(self):
        return super(ManagersManager, self).get_queryset().filter(role__gte=Member.MANAGER)


class Member(ApplicationUser):

    NOT_DEFINED = 0
    MANAGER = 8
    CLIENT = 1

    positions = (
        (MANAGER, 'Manager'),
        (CLIENT, 'Driver'),
        (NOT_DEFINED, 'OUT_OF_ROLE')
    )

    role = models.PositiveIntegerField(default=NOT_DEFINED, choices=positions)
    objects = MemberManager()
    clients = ClientsManager()
    managers = ManagersManager()

    class Meta:
        verbose_name = 'member'

    def __unicode__(self):
        return u'{role} {name}'.format(role=self.get_role_display(), name=self.get_full_name())

    @property
    def is_manager(self):
        return self.role & self.MANAGER

    @property
    def is_client(self):
        return self.role & self.CLIENT
