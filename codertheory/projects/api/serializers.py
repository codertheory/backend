from rest_framework import serializers

from codertheory.projects import models


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Project
        fields = "__all__"


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Task
        fields = "__all__"


class TaskBoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TaskBoard
        fields = "__all__"
