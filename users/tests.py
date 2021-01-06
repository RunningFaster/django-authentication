from django.test import TestCase

# Create your tests here.

import sys
import os

pwd = os.path.dirname(os.path.realpath(__file__))
sys.path.append(pwd + '../')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_auth_admin.settings')

import django

django.setup()

from users.models import Role, Menu, RoleMenu

menu_list = Menu.objects.values_list('id', flat=True).all()
c = []
for i in menu_list:
    c.append(
        RoleMenu(**dict(
            role=1,
            menu=i,
            create_user=1,
            update_user=1
        ))
    )
RoleMenu.objects.bulk_create(c)
