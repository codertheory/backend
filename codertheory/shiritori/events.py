from enum import Enum


class ShiritoriEvents(Enum):
    LobbyCreated = "lobby_created"
    GameCreated = "game_created"
    GameUpdated = "game_updated"
    GameStarted = "game_started"
    GameDeleted = "game_deleted"
    GameFinished = "game_finished"
    PlayerCreated = "player_created"
    PlayerUpdated = "player_updated"
    PlayerDeleted = "player_deleted"
    TurnTaken = "turn_taken"

    def __repr__(self):
        return self.value

    def __str__(self):
        return self.value
