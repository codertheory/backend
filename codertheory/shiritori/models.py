import random
import string
import typing
from typing import Optional

import enchant
from django.db import models
from django.db.models import QuerySet

from codertheory.general.models import BaseModel
from codertheory.shiritori import exceptions

__all__ = (
    "random_letter_generator",
    "ShiritoriGame",
    "ShiritoriPlayer",
    "ShiritoriGameWord"
)


def random_letter_generator():
    return random.choice(string.ascii_lowercase)


# Create your models here.

class ShiritoriGame(BaseModel):
    name = models.CharField(max_length=512)
    password = models.CharField(max_length=5, blank=True, null=True)
    started = models.BooleanField(default=False)
    current_player: Optional["ShiritoriPlayer"] = models.ForeignKey("ShiritoriPlayer", on_delete=models.CASCADE,
                                                                    blank=True, null=True,
                                                                    related_name="current_player_game")
    last_word = models.CharField(max_length=512, null=True, default=random_letter_generator)
    finished = models.BooleanField(default=False)
    timer = models.PositiveSmallIntegerField(default=60)
    winner: Optional["ShiritoriPlayer"] = models.ForeignKey("ShiritoriPlayer", on_delete=models.CASCADE, blank=True,
                                                            null=True,
                                                            related_name="game_winner")

    def start(self):
        self.started = True
        self.save()

    def is_current_player(self, player_id) -> bool:
        return player_id == self.current_player_id

    def join(self, name) -> "ShiritoriPlayer":
        return ShiritoriPlayer.objects.create(
            name=name, game=self
        )

    def leave(self, player_id):
        return ShiritoriPlayer.objects.get(game=self, id=player_id).delete()

    @staticmethod
    def is_real_word(word: str) -> bool:
        d = enchant.Dict("en_US")
        return d.check(word)

    def word_uses_last_letter(self, word: str) -> bool:
        return word.lower().startswith(self.last_word.lower()[-1])

    def word_not_already_used(self, word: str) -> bool:
        queryset = ShiritoriGameWord.objects.filter(game=self, word=word)
        return not queryset.exists()

    def is_valid_word(self, word) -> bool:
        if not self.is_real_word(word):
            raise exceptions.NotRealWordException(word)
        if not self.word_uses_last_letter(word):
            raise exceptions.WordDoesntStartWithLastLetterException(word)
        if not self.word_not_already_used(word):
            raise exceptions.WordAlreadyUsedException(word)
        return True

    @staticmethod
    def calculate_word_score(word: str):
        return round(len(word) * 1.25)

    def take_turn(self, word: str) -> "ShiritoriPlayer":
        try:
            if self.is_valid_word(word):
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
                return self.current_player
        except exceptions.PenaltyException:
            self.current_player.lose_life()
            if self.current_player.is_dead:
                self.select_next_player()
            return self.current_player

    def select_next_player(self):
        self.current_player = self.get_next_player()
        self.save()

    def finish(self):
        self.finished = True
        self.winner = self.current_player
        self.save()

    def get_next_player(self):
        player: typing.Optional["ShiritoriPlayer"] = self.current_player.get_next_in_order()
        while player.is_dead and player != self.current_player:
            player = player.get_next_in_order()
        return player

    def get_previous_player(self):
        player: typing.Optional["ShiritoriPlayer"] = self.current_player.get_previous_in_order()
        while player.is_dead and player != self.current_player:
            player = self.get_previous_in_order()
        return player

    @property
    def players(self) -> QuerySet["ShiritoriPlayer"]:
        # noinspection PyUnresolvedReferences
        order_wrt = ShiritoriPlayer._meta.order_with_respect_to
        filter_args = order_wrt.get_forward_related_filter(self)
        return ShiritoriPlayer.objects.filter(**filter_args)


class ShiritoriPlayer(BaseModel):
    name = models.CharField(max_length=512)
    score = models.IntegerField(default=100)
    game: Optional["ShiritoriGame"] = models.ForeignKey(ShiritoriGame, on_delete=models.CASCADE)
    lives = models.PositiveSmallIntegerField(default=3)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["game", "name"], name="unique_name_per_game"),
            models.UniqueConstraint(fields=["game", "id"], name="unique_player_per_game"),
        ]
        order_with_respect_to = "game"

    @property
    def is_dead(self):
        return self.lives == 0

    def update_points(self, points: int):
        self.score -= points
        self.save()

    def lose_life(self):
        self.lives -= 1
        self.save()


class ShiritoriGameWord(BaseModel):
    word = models.CharField(max_length=512)
    game: "ShiritoriGame" = models.ForeignKey(ShiritoriGame, on_delete=models.CASCADE)
    player: "ShiritoriPlayer" = models.ForeignKey(ShiritoriPlayer, on_delete=models.DO_NOTHING)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["word", "game"], name="unique_word_per_game")
        ]
        order_with_respect_to = "game"
