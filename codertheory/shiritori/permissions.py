from rest_framework import permissions, generics
from rest_framework.generics import get_object_or_404

from . import models

__all__ = (
    "CanJoinGamePermission",
    "GameCanStartPermission",
    "GameCurrentPlayerPermission",
    "GameHasStartedPermission",
)


class CanJoinGamePermission(permissions.BasePermission):

    def has_permission(self, request, view):
        password = request.data.get('password', "")
        pk = view.kwargs.get(view.lookup_url_kwarg)
        view.game = get_object_or_404(models.ShiritoriGame, pk=pk)
        if view.game.password:
            if view.game.password != password:
                self.message = "Invalid Game Password"
            return password == view.game.password and not view.game.started
        return not view.game.started


class GameCanStartPermission(permissions.BasePermission):

    def has_permission(self, request, view: generics.GenericAPIView):
        pk = view.kwargs.get(view.lookup_url_kwarg)
        view.game = get_object_or_404(models.ShiritoriGame, pk=pk)
        if view.game.players.count() < 2:
            self.message = "A Game requires 2 or more players to start"
        return view.game.players.count() >= 2 and not view.game.started


class GameCurrentPlayerPermission(permissions.BasePermission):
    message = "Not Current Player"

    def has_permission(self, request, view: generics.GenericAPIView):
        pk = view.kwargs.get(view.lookup_url_kwarg)
        player = request.data.get('player')
        view.game = get_object_or_404(models.ShiritoriGame, pk=pk)
        return player == str(view.game.current_player_id)


class GameHasStartedPermission(permissions.BasePermission):
    message = "Game Has Not Started"

    def has_permission(self, request, view: generics.GenericAPIView):
        pk = view.kwargs.get(view.lookup_url_kwarg)
        view.game = get_object_or_404(models.ShiritoriGame, pk=pk)
        return view.game.started

