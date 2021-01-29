from rest_framework import permissions, generics

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
        view.game = models.ShiritoriGame.objects.get(pk=pk)
        if view.game.password:
            return password == view.game.password
        return True


class GameCanStartPermission(permissions.BasePermission):

    def has_permission(self, request, view: generics.GenericAPIView):
        pk = view.kwargs.get(view.lookup_url_kwarg)
        view.game = models.ShiritoriGame.objects.get(pk=pk)
        return view.game.players.count() >= 2 and not view.game.started


class GameCurrentPlayerPermission(permissions.BasePermission):

    def has_permission(self, request, view: generics.GenericAPIView):
        pk = view.kwargs.get(view.lookup_url_kwarg)
        player = request.data.get('player')
        view.game = models.ShiritoriGame.objects.get(pk=pk)
        return player == str(view.game.current_player_id)


class GameHasStartedPermission(permissions.BasePermission):

    def has_permission(self, request, view: generics.GenericAPIView):
        pk = view.kwargs.get(view.lookup_url_kwarg)
        view.game = models.ShiritoriGame.objects.get(pk=pk)
        return view.game.started


class PlayerInGamePermission(permissions.BasePermission):

    def has_permission(self, request, view: generics.GenericAPIView):
        player_id = request.data.get('id')
        game_id = view.kwargs.get(view.lookup_url_kwarg)
        view.game = models.ShiritoriGame.objects.get(pk=game_id)
        return models.ShiritoriPlayer.objects.filter(game_id=game_id, id=player_id).exists()
