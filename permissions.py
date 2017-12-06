from django.contrib.auth.models import Group, Permission

g, _ = Group.objects.get_or_create(name='bank_admin')

account_p = Permission.objects.filter(name__icontains='account')
card_p = Permission.objects.filter(name__icontains='card')
member_p = Permission.objects.filter(codename='change_member')
currencyrate_p = Permission.objects.filter(codename__icontains='currencyrate')

for permission_set in [account_p, card_p, member_p, currencyrate_p]:
    for permission in permission_set:
        g.permissions.add(permission)
