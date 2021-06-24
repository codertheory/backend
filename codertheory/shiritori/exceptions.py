__all__ = (
    "GameException",
    "PenaltyException",
    "NotRealWordException",
    "WordDoesntStartWithLastLetterException",
    "WordAlreadyUsedException",
)


class GameException(Exception):
    pass


class PenaltyException(GameException):
    def __init__(self, word=None, msg=None):
        self.word = word
        super(PenaltyException, self).__init__(msg)


class NotRealWordException(PenaltyException):

    def __init__(self, word):
        super(NotRealWordException, self).__init__(word, f"{word} is not a valid English Word")


class WordDoesntStartWithLastLetterException(PenaltyException):

    def __init__(self, word):
        self.word = word
        super(WordDoesntStartWithLastLetterException, self).__init__(word,
                                                                     f"{word} doesnt start with the same letter as "
                                                                     f"last used word")


class WordAlreadyUsedException(PenaltyException):
    def __init__(self, word):
        self.word = word
        super(WordAlreadyUsedException, self).__init__(word, f"{word} Already used this game")


class BlankInputGivenException(PenaltyException):
    def __init__(self):
        super(BlankInputGivenException, self).__init__(msg="No Input Given")


class NotEnoughPlayersException(GameException):
    def __init__(self, game):
        self.game = game
        super(NotEnoughPlayersException, self).__init__("A Game requires at least 2 players to start")


class GameCannotStartException(GameException):
    def __init__(self, game):
        self.game = game
        super(GameCannotStartException, self).__init__(f"{game} - Cannot start")


class GameAlreadyFinishedException(GameException):
    pass
