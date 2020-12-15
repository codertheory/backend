from pinax.blog import models
from rest_framework import serializers


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Post
        fields = "__all__"


class TagSerializer(serializers.ModelSerializer):
    pass


class CommentSerializer(serializers.ModelSerializer):
    pass
