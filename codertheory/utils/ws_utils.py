from enum import Enum

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

__all__ = (
    "EventsEnum",
    "send_data_to_channel",
)

from graphene.utils.str_converters import to_snake_case


class EventsEnum(Enum):

    def __repr__(self):
        return self.value

    def __str__(self):
        return self.value

    def __eq__(self, other):
        if isinstance(other, str):
            return str(self) == to_snake_case(other)
        else:
            return super(EventsEnum, self).__eq__(other)


def send_data_to_channel(name: str, data: dict, *, group_send: bool = True):
    if "type" in data:
        data['type'] = str(data['type'])
    channel_layer = get_channel_layer()
    coro = async_to_sync(channel_layer.group_send if group_send else channel_layer.send)
    coro(name, data)
