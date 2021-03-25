from codertheory.utils.ws_utils import EventsEnum


class ShiritoriEvents(EventsEnum):
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
    TimerCountDown = "timer_count_down"
    TimerFinished = "timer_finished"
    Unknown = "unknown"
