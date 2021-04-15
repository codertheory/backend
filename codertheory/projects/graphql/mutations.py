from graphene_django.rest_framework.mutation import SerializerMutation

from . import serializers


class ProjectMutation(SerializerMutation):
    class Meta:
        serializer_class = serializers.ProjectSerializer
        convert_choices_to_enum = False
