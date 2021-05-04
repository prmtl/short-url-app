from functools import partial

from django.contrib.admin import AdminSite as _AdminSite
from django.contrib.admin import register


class AdminSite(_AdminSite):
    pass


admin_site = AdminSite(name="admin")
register = partial(register, site=admin_site)
