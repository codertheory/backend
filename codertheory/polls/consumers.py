from codertheory.general.consumers import EntityJsonConsumer
from codertheory.polls import models, events
from codertheory.polls.api import serializers


class PollConsumer(EntityJsonConsumer):
    url_kwarg = "poll"
    queryset = models.Poll.objects

    def websocket_connect(self, message):
        super(PollConsumer, self).websocket_connect(message)
        poll = self.get_model()
        self.send_json({
            "type": events.PollEvents.Connect,
            "poll": serializers.PollSerializer(poll).data
        })

    def websocket_disconnect(self, message):
        super(PollConsumer, self).websocket_disconnect(message)

    def poll_vote(self, event: dict):
        self.send_json(event)
