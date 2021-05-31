from rest_framework import serializers, exceptions

from codertheory.polls import models

__all__ = (
    "PollOptionSerializer",
    "PollSerializer",
)


class PollOptionSerializer(serializers.ModelSerializer):
    poll_id = serializers.CharField(write_only=True)
    votes = serializers.IntegerField(read_only=True, source="vote_count")

    class Meta:
        model = models.PollOption
        fields = ("poll_id", "option", "votes")


class PollSerializer(serializers.ModelSerializer):
    options = PollOptionSerializer(read_only=True, many=True)
    vote_count = serializers.IntegerField(read_only=True, source="total_vote_count")

    class Meta:
        model = models.Poll
        fields = "__all__"

    def create(self, validated_data):
        try:
            options = self.initial_data.pop("options")
        except KeyError as error:
            raise exceptions.ParseError({"options": self.fields['options'].default_error_messages['empty']}) from error
        poll = super().create(validated_data)
        options_list = []
        for index, option_dict in enumerate(options):
            option_dict['poll_id'] = poll.id
            option_serializer = PollOptionSerializer(data=option_dict)
            if option_serializer.is_valid():
                options_list.append(models.PollOption(**option_dict, _order=index))
        models.PollOption.objects.bulk_create(options_list)
        return poll
