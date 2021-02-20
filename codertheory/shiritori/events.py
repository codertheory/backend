from enum import Enum

from graphene.utils.str_converters import to_snake_case


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
    TimerCountDown = "timer_countdown"
    TimerFinished = "timer_finished"

    def __repr__(self):
        return self.value

    def __str__(self):
        return self.value

    def __eq__(self, other):
        if isinstance(other, str):
            return str(self) == to_snake_case(other)
        else:
            return super(ShiritoriEvents, self).__eq__(other)
