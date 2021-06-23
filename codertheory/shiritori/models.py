import itertools
import random
import string
from typing import Optional

import enchant
from auditlog.registry import auditlog
from django.db import models
from django.db.models import QuerySet

from codertheory.general.models import BaseModel
from codertheory.shiritori import exceptions
from codertheory.shiritori import utils

__all__ = (
    "random_letter_generator",
    "ShiritoriGame",
    "ShiritoriPlayer",
    "ShiritoriGameWord"
)


def random_letter_generator():
    return random.choice(string.ascii_lowercase)


TIMEOUT_POINTS_GAIN = 10


# Create your models here.

class ShiritoriGame(BaseModel):
    password = models.CharField(max_length=5, blank=True, null=True)
    started = models.BooleanField(default=False)
    current_player: Optional["ShiritoriPlayer"] = models.ForeignKey("ShiritoriPlayer", on_delete=models.CASCADE,
                                                                    blank=True, null=True,
                                                                    related_name="current_player_game")
    last_word = models.CharField(max_length=512, null=True, default=random_letter_generator)
    finished = models.BooleanField(default=False)
    timer = models.PositiveSmallIntegerField(default=10)
    winner: Optional["ShiritoriPlayer"] = models.ForeignKey("ShiritoriPlayer", on_delete=models.CASCADE, blank=True,
                                                            null=True,
                                                            related_name="game_winner")
    player_index = models.PositiveSmallIntegerField(default=0)
    last_edited = models.DateTimeField(auto_now=True)

    def start(self, *, ignore_count: bool = False):
        if self.players.count() >= 2 or ignore_count:
            self.started = True
            try:
                self.current_player = self.players[0]
            except IndexError:
                pass
            ShiritoriGame.objects.filter(id=self.id).update(started=self.started, current_player=self.current_player)
            utils.send_start_game_event(self)
        else:
            raise exceptions.GameCannotStartException(self)

    def finish(self):
        self.started = True
        self.finished = True
        self.winner = self.current_player
        ShiritoriGame.objects.filter(id=self.id).update(started=self.started, finished=self.finished,
                                                        winner=self.winner)
        utils.send_finish_game_event(self)

    def is_current_player(self, player_id) -> bool:
        return player_id == self.current_player_id

    def join(self, name) -> "ShiritoriPlayer":
        new_player = ShiritoriPlayer.objects.create(
            name=name, game=self
        )
        utils.send_player_joined_or_left_event(self)
        return new_player

    def leave(self, player_id):
        old_player = ShiritoriPlayer.objects.get(id=player_id).delete()
        utils.send_player_joined_or_left_event(self)
        return old_player

    @staticmethod
    def is_real_word(word: str) -> bool:
        d = enchant.Dict("en_US")
        return d.check(word)

    def word_uses_last_letter(self, word: str) -> bool:
        return word.lower().startswith(self.last_word.lower()[-1])

    def word_not_already_used(self, word: str) -> bool:
        queryset = ShiritoriGameWord.objects.filter(game=self, word=word)
        return not queryset.exists()

    def validate_word(self, word):
        if not word:
            raise exceptions.BlankInputGivenException()
        if not self.is_real_word(word):
            raise exceptions.NotRealWordException(word)
        if not self.word_not_already_used(word):
            raise exceptions.WordAlreadyUsedException(word)
        if not self.word_uses_last_letter(word):
            raise exceptions.WordDoesntStartWithLastLetterException(word)

    @staticmethod
    def calculate_word_score(word: str):
        return round(len(word) * 1.25)

    def take_turn(self, word: str = None, *, raise_exception: bool = True):
        if self.finished:
            if raise_exception:
                raise exceptions.GameAlreadyFinishedException
            else:
                return
        try:
            self.validate_word(word)
            word_score = self.calculate_word_score(word)
            ShiritoriGameWord.objects.create(
                word=word.lower(), game=self, player=self.current_player
            )
            self.current_player.update_points(word_score)
            self.last_word = word
            if self.current_player.score <= 0:
                self.finish()
            else:
                self.select_next_player()
        except exceptions.PenaltyException as error:
            if self.current_player is not None:
                self.current_player.gain_points()
            if not isinstance(error, exceptions.BlankInputGivenException):
                if raise_exception:
                    raise error
            self.select_next_player()
        finally:
            if not self.finished:
                self.save()
            utils.send_turn_taken_event(self)

    def select_next_player(self):
        next_player = self.get_next_player()
        self.current_player = next_player

    def get_next_player(self):
        player_count = self.players.count()
        if self.player_index > player_count and (self.player_index + 1) > player_count:
            self.player_index = 0
        else:
            self.player_index += 1
        player = next(itertools.islice(itertools.cycle(self.players), self.player_index, None))
        return player

    @property
    def players(self) -> QuerySet["ShiritoriPlayer"]:
        # noinspection PyUnresolvedReferences
        order_wrt = ShiritoriPlayer._meta.order_with_respect_to
        filter_args = order_wrt.get_forward_related_filter(self)
        return ShiritoriPlayer.objects.filter(**filter_args)

    @property
    def host(self) -> QuerySet["ShiritoriPlayer"]:
        return self.players.first()

    @property
    def is_finished(self):
        return all([self.finished, self.started])


class ShiritoriPlayer(BaseModel):
    name = models.CharField(max_length=512)
    score = models.IntegerField(default=100)
    game: Optional["ShiritoriGame"] = models.ForeignKey(ShiritoriGame, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["game", "name"], name="unique_name_per_game"),
            models.UniqueConstraint(fields=["game", "id"], name="unique_player_per_game"),
        ]
        order_with_respect_to = "game"

    @property
    def is_current(self):
        return self == self.game.current_player

    @property
    def words(self):
        return ShiritoriGameWord.objects.filter(game=self.game, player=self)

    def update_points(self, points: int):
        self.score -= points
        self.save()

    def gain_points(self):
        self.score += TIMEOUT_POINTS_GAIN
        self.save()

    def leave(self):
        return self.game.leave(self.id)


class ShiritoriGameWord(BaseModel):
    word = models.CharField(max_length=512)
    game: "ShiritoriGame" = models.ForeignKey(ShiritoriGame, on_delete=models.CASCADE)
    player: "ShiritoriPlayer" = models.ForeignKey(ShiritoriPlayer, on_delete=models.DO_NOTHING)

    @property
    def score(self):
        return ShiritoriGame.calculate_word_score(self.word)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["word", "game"], name="unique_word_per_game")
        ]
        order_with_respect_to = "game"


auditlog.register(ShiritoriGame, include_fields=("started", "winner"))
