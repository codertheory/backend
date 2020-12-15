from graphene_django.rest_framework.mutation import SerializerMutation

from . import serializers


class PostMutation(SerializerMutation):
    class Meta:
        serializer_class = serializers.PostSerializer
        convert_choices_to_enum = False

# TODO create these serializers/mutations
# class TagMutation(SerializerMutation):
#     class Meta:
#         serializer_class = serializers.TagSerializer
#
#
# class CommentMutation(SerializerMutation):
#     class Meta:
#         serializer_class = serializers.CommentSerializer
