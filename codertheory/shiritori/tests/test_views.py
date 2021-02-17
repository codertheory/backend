from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from codertheory.shiritori import models
from . import factories


class ShiritoriViewTests(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.game: models.ShiritoriGame = factories.GameFactory()

    def test_create_game(self):
        url = reverse("api:api_version_1:shiritori_game-list")
        data = {
            "name": "foobar",
            "password": "1234"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)

    def test_join_game(self):
        url = reverse("api:api_version_1:shiritori_game-join", kwargs={"pk": self.game.id})
        data = {
            "name": "foobar"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 202)

    def test_join_game_already_started(self):
        self.game.save(update_fields={"started": True})
        url = reverse("api:api_version_1:shiritori_game-join", kwargs={"pk": self.game.id})
        data = {
            "name": "foobar"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 403)

    def test_leave_game(self):
        player = self.game.join("foobar")
        url = reverse("api:api_version_1:shiritori_game-leave", kwargs={"pk": player.game.id})
        data = {
            "id": player.id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 204)

    def test_start_game(self):
        self.game.join("p1")
        self.game.join("p2")
        url = reverse("api:api_version_1:shiritori_game-start", kwargs={"pk": self.game.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.game.refresh_from_db()
        self.assertTrue(self.game.started)

    def test_start_game_already_started(self):
        self.game.save(update_fields={"started": True})
        url = reverse("api:api_version_1:shiritori_game-start", kwargs={"pk": self.game.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 403)

    def test_finish_game(self):
        self.game.start()
        url = reverse("api:api_version_1:shiritori_game-finish", kwargs={"pk": self.game.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.game.refresh_from_db()
        self.assertTrue(self.game.finished)

    def test_take_game_turn(self):
        player = factories.PlayerFactory(game=self.game)
        self.game.current_player = player
        self.game.save()
        url = reverse("api:api_version_1:shiritori_game-take-turn", kwargs={"pk": self.game.id})
        data = {
            "word": "bar",
            "player": player.id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
