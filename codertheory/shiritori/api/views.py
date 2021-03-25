import sys
import traceback
import typing

from rest_framework import permissions
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from codertheory.shiritori import models, exceptions
from codertheory.shiritori.api import serializers
from codertheory.shiritori.permissions import *

__all__ = (
    "GameModelViewSet",
)


# TODO document actions properly

class GameModelViewSet(viewsets.ModelViewSet):
    queryset = models.ShiritoriGame.objects.all()
    serializer_class = serializers.GameSerializer
    lookup_url_kwarg = "pk"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.game: typing.Optional[models.ShiritoriGame] = None

    def get_permissions(self):
        if self.action in ['list', 'create']:
            self.permission_classes = [permissions.AllowAny]
        return super(GameModelViewSet, self).get_permissions()

    @action(name="create", url_name="create", url_path="create", methods=['post'], detail=False,
            permission_classes=[permissions.AllowAny],
            authentication_classes=[])
    def create_game(self, request, **kwargs):
        return self.create(request, **kwargs)

    @action(name="join", url_name="join", url_path="join", methods=['post'], detail=True,
            permission_classes=[CanJoinGamePermission],
            authentication_classes=[])
    def join_game(self, request, pk=None):
        player_name = request.data.get("name")
        player = self.game.join(player_name)
        return Response(status=status.HTTP_202_ACCEPTED, data=serializers.PlayerSerializer(player).data)

    @action(name="leave", url_name="leave", url_path="leave", methods=['delete'], detail=True,
            permission_classes=[],
            authentication_classes=[])
    def leave_game(self, request, pk=None):
        player = request.data.get('id')
        try:
            game = models.ShiritoriGame.objects.get(pk=pk)
            game.leave(player)
        except models.ShiritoriGame.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(name="start", url_name="start", url_path="start", methods=['post'], detail=True,
            permission_classes=[GameCanStartPermission],
            authentication_classes=[])
    def start_game(self, request, pk=None):
        self.game.start()
        return Response(status=status.HTTP_200_OK)

    @action(name="end", url_name="finish", url_path="finish", methods=['post'], detail=True,
            permission_classes=[GameHasStartedPermission],
            authentication_classes=[])
    def finish_game(self, request, pk=None):
        self.game.finish()
        return Response(status=status.HTTP_200_OK)

    @action(name="take-turn", url_name="take-turn", url_path="take-turn", methods=['post'], detail=True,
            permission_classes=[GameHasStartedPermission],
            authentication_classes=[], throttle_classes=[])
    def take_game_turn(self, request, pk=None):
        word: str = request.data.get('word', "")
        try:
            self.game.take_turn(word)
            return Response(status=status.HTTP_200_OK)
        except exceptions.GameAlreadyFinishedException:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        except exceptions.GameException as error:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": str(error)})
        except Exception as error:
            print('Ignoring exception in View {}:'.format(self), file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data={"error": str(error)})

    @action(name='generate', url_name="generate", url_path="generate", methods=['post'],
            permission_classes=[IsAdminUser], detail=False)
    def generate_game(self, request):
        game = models.ShiritoriGame.objects.create()
        game.join("x")
        game.join("y")
        game.start()
        return Response(status=status.HTTP_201_CREATED)
