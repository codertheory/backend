from rest_framework import permissions, generics
from rest_framework.generics import get_object_or_404

from . import models

__all__ = (
    "GamePasswordPermission",
    "GameCanStartPermission",
    "GameCurrentPlayerPermission",
    "GameHasStartedPermission",
    "PlayerInGamePermission"
)


class GamePasswordPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        password = request.data.get('password', "")
        pk = view.kwargs.get(view.lookup_url_kwarg)
        view.game = get_object_or_404(models.ShiritoriGame, pk=pk)
        if view.game.password:
            return password == view.game.password
        return True


class GameCanStartPermission(permissions.BasePermission):

    def has_permission(self, request, view: generics.GenericAPIView):
        pk = view.kwargs.get(view.lookup_url_kwarg)
        view.game = get_object_or_404(models.ShiritoriGame, pk=pk)
        return view.game.players.count() >= 2 and not view.game.started


class GameCurrentPlayerPermission(permissions.BasePermission):

    def has_permission(self, request, view: generics.GenericAPIView):
        pk = view.kwargs.get(view.lookup_url_kwarg)
        player = request.data.get('player')
        view.game = get_object_or_404(models.ShiritoriGame, pk=pk)
        return player == str(view.game.current_player_id)


class GameHasStartedPermission(permissions.BasePermission):

    def has_permission(self, request, view: generics.GenericAPIView):
        pk = view.kwargs.get(view.lookup_url_kwarg)
        view.game = get_object_or_404(models.ShiritoriGame, pk=pk)
        return view.game.started


class PlayerInGamePermission(permissions.BasePermission):

    def has_permission(self, request, view: generics.GenericAPIView):
        player_id = request.data.get('id')
        pk = view.kwargs.get(view.lookup_url_kwarg)
        view.game = get_object_or_404(models.ShiritoriGame, pk=pk)
        return models.ShiritoriPlayer.objects.filter(game_id=pk, id=player_id).exists()
