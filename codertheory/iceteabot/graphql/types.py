from graphene_django import DjangoObjectType

from codertheory.iceteabot import models


class ActivityType(DjangoObjectType):
    class Meta:
        model = models.Activity
        fields = "__all__"


class DiscordChannelType(DjangoObjectType):
    class Meta:
        model = models.DiscordChannel
        fields = "__all__"


class CommandCallType(DjangoObjectType):
    class Meta:
        model = models.CommandCall
        fields = "__all__"


class FAQType(DjangoObjectType):
    class Meta:
        model = models.FAQ
        fields = "__all__"


class DiscordResponseType(DjangoObjectType):
    class Meta:
        model = models.DiscordResponse
        fields = "__all__"


class DiscordGuildType(DjangoObjectType):
    class Meta:
        model = models.DiscordGuild
        fields = "__all__"


class DiscordMemberType(DjangoObjectType):
    class Meta:
        model = models.DiscordMember
        fields = "_all__"


class DiscordNickNameType(DjangoObjectType):
    class Meta:
        model = models.DiscordNickName
        fields = "__all__"


class CommandPrefixType(DjangoObjectType):
    class Meta:
        model = models.CommandPrefix
        fields = "__all__"


class ReactionRoleType(DjangoObjectType):
    class Meta:
        model = models.ReactionRole
        fields = "__all__"


class ReminderType(DjangoObjectType):
    class Meta:
        model = models.Reminder
        fields = "__all__"


class TagType(DjangoObjectType):
    class Meta:
        model = models.Tag
        fields = "__all__"


class TagLookUpType(DjangoObjectType):
    class Meta:
        model = models.TagLookUp
        fields = "__all__"


class TagCallType(DjangoObjectType):
    class Meta:
        model = models.TagCall
        fields = "__all__"


class TaskType(DjangoObjectType):
    class Meta:
        model = models.Task
        fields = "__all__"


class DiscordUserType(DjangoObjectType):
    class Meta:
        model = models.DiscordUser
        fields = "__all__"
