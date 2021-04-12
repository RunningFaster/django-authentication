from django.apps import AppConfig

default_app_config = "organization.apps.OrganizationConfig"


class OrganizationConfig(AppConfig):
    name = 'organization'
    verbose_name = "组织架构"
