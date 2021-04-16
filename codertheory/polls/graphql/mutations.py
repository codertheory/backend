from graphene_django.rest_framework.mutation import SerializerMutation

from . import serializers


class PollMutation(SerializerMutation):
    class Meta:
        serializer_class = serializers.PollSerializer
        convert_choices_to_enum = False
