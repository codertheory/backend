import typing

from codertheory.shiritori import models


class LobbyCreateDataPayload(typing.TypedDict):
    games: typing.List[models.ShiritoriGame]


class GameCreatedDataPayload(typing.TypedDict):
    game: models.ShiritoriGame


class GameUpdatedDataPayload(typing.TypedDict):
    game: models.ShiritoriGame


class GameStartedDataPayload(typing.TypedDict):
    game: models.ShiritoriGame


class GameDeletedDataPayload(typing.TypedDict):
    game: models.ShiritoriGame


class GameFinishedDataPayload(typing.TypedDict):
    game: models.ShiritoriGame


class PlayerCreatedDataPayload(typing.TypedDict):
    player: models.ShiritoriPlayer


class PlayerUpdatedDataPayload(typing.TypedDict):
    player: models.ShiritoriPlayer


class PlayerDeletedDataPayload(typing.TypedDict):
    player: models.ShiritoriPlayer


class TurnTakenDataPayload(typing.TypedDict):
    player: typing.AnyStr
    word: typing.AnyStr
