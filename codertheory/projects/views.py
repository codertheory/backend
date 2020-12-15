from django.views import generic

from codertheory.projects import models


class ProjectView(generic.DetailView):
    template_name = "website/pages/project.html"
    queryset = models.Project.objects.all()
    context_object_name = "project"
