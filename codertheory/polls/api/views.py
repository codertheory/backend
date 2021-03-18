from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from codertheory.polls import models
from codertheory.polls.api import serializers

__all__ = (
    "PollViewSet",
)


class PollViewSet(viewsets.ModelViewSet):
    queryset = models.Poll.objects.all()
    serializer_class = serializers.PollSerializer
    authentication_classes = []
    permission_classes = []

    @action(name="vote", url_name="vote", url_path="vote", methods=['post'], detail=True, description="Vote on a poll")
    def vote(self,request, pk=None):
        option_id = request.POST.get('option')
        poll: models.Poll = self.get_object()
        option = poll.get_option(option_id)
        option.vote(self.request)
        return Response(status=status.HTTP_201_CREATED)
