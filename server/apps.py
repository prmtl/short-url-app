from django.contrib.admin.apps import AdminConfig as _AdminConfig


class AdminConfig(_AdminConfig):
    default_site = "server.admin.AdminSite"
