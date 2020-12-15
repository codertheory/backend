from rest_framework import viewsets

from codertheory.projects import models
from codertheory.projects.api import serializers


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ProjectSerializer
    queryset = models.Project.objects.all()


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.TaskSerializer
    queryset = models.Task.objects.all()


class TaskBoardViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.TaskBoardSerializer
    queryset = models.TaskBoard.objects.all()
