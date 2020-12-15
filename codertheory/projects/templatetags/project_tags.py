from django import template

from codertheory.projects import models

register = template.Library()


@register.simple_tag()
def projects():
    return models.Project.objects.all().filter(status=models.ProjectStatus.ACTIVE)
