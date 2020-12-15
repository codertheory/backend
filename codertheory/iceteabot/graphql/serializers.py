from rest_framework import serializers

from codertheory.iceteabot import models


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Activity
        fields = "__all__"


class DiscordChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DiscordChannel
        fields = "__all__"


class CommandCallSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CommandCall
        fields = "__all__"


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FAQ
        fields = "__all__"


class DiscordResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DiscordResponse
        fields = "__all__"


class DiscordGuildSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DiscordGuild
        fields = "__all__"


class DiscordMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DiscordMember
        fields = "_all__"


class DiscordNickNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DiscordNickName
        fields = "__all__"


class CommandPrefixSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CommandPrefix
        fields = "__all__"


class ReactionRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ReactionRole
        fields = "__all__"


class ReminderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Reminder
        fields = "__all__"


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tag
        fields = "__all__"


class TagLookUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TagLookUp
        fields = "__all__"


class TagCallSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TagCall
        fields = "__all__"


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Task
        fields = "__all__"


class DiscordUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DiscordUser
        fields = "__all__"
