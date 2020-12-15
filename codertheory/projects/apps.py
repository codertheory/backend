from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ProjectsConfig(AppConfig):
    name = 'codertheory.projects'
    verbose_name = _("Projects")
