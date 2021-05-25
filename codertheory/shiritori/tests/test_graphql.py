from unittest import skip

from graphene_django.utils.testing import GraphQLTestCase
from rest_framework.reverse import reverse

from codertheory.shiritori import models
from . import factories


@skip("Refactor to Graphql")
class ShiritoriGraphQLTests(GraphQLTestCase):

    @classmethod
    def setUpTestData(cls):
        cls.game: models.ShiritoriGame = factories.GameFactory()

    def test_create_game(self):
        url = reverse("api:v1:shiritori_game-list")
        data = {
            "name": "foobar",
            "password": "1234"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)

    def test_join_game(self):
        url = reverse("api:v1:shiritori_game-join", kwargs={"pk": self.game.id})
        data = {
            "name": "foobar"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 202)

    def test_join_game_already_started(self):
        self.game.save(update_fields={"started": True})
        url = reverse("api:v1:shiritori_game-join", kwargs={"pk": self.game.id})
        data = {
            "name": "foobar"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 403)

    def test_leave_game(self):
        player = self.game.join("foobar")
        url = reverse("api:v1:shiritori_game-leave", kwargs={"pk": player.game.id})
        data = {
            "id": player.id
        }
        response = self.client.delete(url, data)
        self.assertEqual(response.status_code, 204)

    def test_start_game(self):
        self.game.join("p1")
        self.game.join("p2")
        url = reverse("api:v1:shiritori_game-start", kwargs={"pk": self.game.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.game.refresh_from_db()
        self.assertTrue(self.game.started)

    def test_start_game_already_started(self):
        self.game.save(update_fields={"started": True})
        url = reverse("api:v1:shiritori_game-start", kwargs={"pk": self.game.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 403)

    def test_finish_game(self):
        factories.PlayerFactory.create_batch(2, game=self.game)
        self.game.start()
        url = reverse("api:v1:shiritori_game-finish", kwargs={"pk": self.game.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.game.refresh_from_db()
        self.assertTrue(self.game.finished)

    def test_take_game_turn(self):
        player = factories.PlayerFactory(game=self.game)
        self.game.current_player = player
        self.game.last_word = "b"
        self.game.started = True
        self.game.save()
        url = reverse("api:v1:shiritori_game-take-turn", kwargs={"pk": self.game.id})
        data = {
            "word": "bar",
            "player": player.id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)

    def test_Take_game_turn_already_finished(self):
        self.game.started = True
        self.game.finished = True
        self.game.save()
        player = factories.PlayerFactory(game=self.game)
        url = reverse("api:v1:shiritori_game-take-turn", kwargs={"pk": self.game.id})
        data = {
            "word": "bar",
            "player": player.id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 406)
