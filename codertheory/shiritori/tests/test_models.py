import uuid

from django.db import IntegrityError
from django.test import TestCase

from codertheory.shiritori import exceptions
from codertheory.shiritori import factories
from codertheory.shiritori import models


class ShiritoriModelTests(TestCase):

    def setUp(self):
        self.player_one: models.ShiritoriPlayer = factories.PlayerFactory()
        self.game: models.ShiritoriGame = self.player_one.game
        # noinspection PyTypeHints
        self.game.current_player: models.ShiritoriPlayer = self.player_one

    def test_start_game(self):
        self.assertFalse(self.game.started)
        self.game.start()
        self.assertTrue(self.game.started)

    def test_is_current_player(self):
        self.assertTrue(self.game.is_current_player(self.player_one.id))

    def test_join_game(self):
        player = self.game.join("Player 2")
        self.assertEqual(player.game, self.game)

    def test_get_next_player(self):
        player_two: models.ShiritoriPlayer = factories.PlayerFactory(game=self.game)
        next_player = self.game.get_next_player()
        self.assertEqual(player_two, next_player)

    def test_get_game_players_in_order(self):
        new_players = factories.PlayerFactory.create_batch(3, game=self.game)
        players = list(self.game.players)
        self.assertEqual(len(players), 4)
        self.assertListEqual(players, [self.game.current_player, *new_players])

    def test_join_game_duplicate_name(self):
        self.assertRaises(IntegrityError, lambda: self.game.join(self.player_one.name))

    def test_leave_game(self):
        response = self.game.leave(self.player_one.id)
        self.assertTrue(response)

    def test_leave_game_invalid_id(self):
        # noinspection PyTypeChecker
        self.assertRaises(models.ShiritoriPlayer.DoesNotExist, lambda: self.game.leave(uuid.uuid4()))

    def test_is_real_word(self):
        self.assertTrue(self.game.is_real_word("Hello"))

    def test_is_real_word_invalid_word(self):
        self.assertFalse(self.game.is_real_word("Hllo"))

    def test_word_startswith_last_letter(self):
        self.game.last_word = "bar"
        self.assertTrue(self.game.word_uses_last_letter("ready"))

    def test_word_doesnt_startswith_last_letter(self):
        self.assertFalse(self.game.word_uses_last_letter("unready"))

    def test_word_not_already_used(self):
        self.assertTrue(self.game.word_not_already_used("bar"))

    def test_word_already_used(self):
        factories.GameWordFactory(
            word="foo",
            game=self.game,
            player=self.player_one
        )
        self.assertFalse(self.game.word_not_already_used("foo"))

    def test_is_valid_word_not_real_word_exception(self):
        self.assertRaises(exceptions.NotRealWordException, lambda: self.game.is_valid_word("helo"))

    def test_is_valid_word_word_doesnt_start_with_last_letter_exception(self):
        self.assertRaises(exceptions.WordDoesntStartWithLastLetterException, lambda: self.game.is_valid_word("Hello"))

    def test_is_valid_word_word_already_used_exception(self):
        factories.GameWordFactory(
            word="radio",
            game=self.game,
            player=self.player_one
        )
        self.assertRaises(exceptions.WordAlreadyUsedException, lambda: self.game.is_valid_word("radio"))

    def test_calculate_word_score(self):
        word_score = self.game.calculate_word_score("foo")
        self.assertGreater(word_score, 0)

    def test_take_turn(self):
        self.game.last_word = "bar"
        factories.PlayerFactory(game=self.game)
        self.assertEqual(self.player_one.score, 100)
        word = "radio"
        self.game.take_turn(word)
        self.assertLess(self.player_one.score, 100)

    def test_take_turn_check_lives(self):
        self.assertEqual(self.player_one.lives, 3)
        word = "air"
        new_player_one = self.game.take_turn(word)
        self.assertEqual(new_player_one.lives, 2)

    def test_take_turn_win_game(self):
        self.game.last_word = "beautiful"
        self.game.current_player.score = 5
        winner_updated = self.game.take_turn("landscaping")
        self.assertTrue(self.game.finished)
        self.assertLessEqual(winner_updated.score, 0)

    def test_take_turn_lose_live(self):
        self.assertEqual(self.player_one.lives, 3)
        updated_player = self.game.take_turn("blah")
        self.assertEqual(updated_player.lives, 2)

    def test_finish(self):
        self.assertFalse(self.game.finished)
        self.game.finish()
        self.assertTrue(self.game.finished)

    def test_update_player_points(self):
        self.player_one.update_points(10)
        self.assertEqual(self.player_one.score, 90)

    def test_player_lose_lives(self):
        self.assertEqual(self.player_one.lives, 3)
        self.player_one.lose_life()
        self.assertEqual(self.player_one.lives, 2)

    def test_run_out_of_lives(self):
        factories.PlayerFactory(game=self.game)
        self.game.current_player.lives = 1
        current_player_id = str(self.game.current_player.id)
        self.game.take_turn("unknown")
        self.assertNotEqual(current_player_id, self.game.current_player.id)
