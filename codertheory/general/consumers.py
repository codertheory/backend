from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from channels.generic.websocket import JsonWebsocketConsumer, AsyncJsonWebsocketConsumer
from django.db import models
from graphene.utils.str_converters import to_camel_case


class AbstractConsumer:
    url_kwarg = ""
    queryset: models.QuerySet = None

    @property
    def target_id(self):
        return self.scope['url_route']['kwargs'][self.url_kwarg]

    @staticmethod
    def _clean_json(content):
        data = {
            "type": to_camel_case(str(content.pop('type', ""))),
            "data": content
        }
        return data


class EntityJsonConsumer(AbstractConsumer, JsonWebsocketConsumer):

    def get_model(self):
        return self.queryset.get(pk=self.target_id)

    def send_json(self, content, close=False):
        return super(EntityJsonConsumer, self).send_json(self._clean_json(content), close)

    def websocket_connect(self, message):
        async_to_sync(self.channel_layer.group_add)(self.target_id, self.channel_name)
        super(EntityJsonConsumer, self).websocket_connect(message)

    def websocket_disconnect(self, message):
        async_to_sync(self.channel_layer.group_discard)(self.target_id, self.channel_name)
        super(EntityJsonConsumer, self).websocket_disconnect(message)


class AsyncEntityJsonConsumer(AbstractConsumer, AsyncJsonWebsocketConsumer):

    @database_sync_to_async
    def get_model(self):
        return self.queryset.get(pk=self.target_id)

    async def send_json(self, content, close=False):
        return await super(AsyncEntityJsonConsumer, self).send_json(self._clean_json(content), close)

    async def websocket_connect(self, message):
        await self.channel_layer.group_add(self.target_id, self.channel_name)
        await super(AsyncEntityJsonConsumer, self).websocket_connect(message)

    async def websocket_disconnect(self, message):
        await self.channel_layer.group_discard(self.target_id, self.channel_name)
        await super(AsyncEntityJsonConsumer, self).websocket_disconnect(message)
