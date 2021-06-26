from unittest import skip

from graphene_django.utils.testing import GraphQLTestCase
from rest_framework.reverse import reverse

from codertheory.shiritori import models
from . import factories


class ShiritoriGraphQLTests(GraphQLTestCase):

    @classmethod
    def setUpTestData(cls):
        cls.game: models.ShiritoriGame = factories.GameFactory()

    def test_create_game(self):
        response = self.query(
            '''
            mutation CreateGame($private: Boolean){
                createGame(private: $private){
                    game {
                        id
                    }
                }
            }

            '''
        )
        self.assertResponseNoErrors(response)

    def test_join_game(self):
        response = self.query(
            '''
            mutation JoinGame($gameId: ID, $playerName: String){
                joinGame(gameId: $gameId, playerName: $playerName){
                    player {
                        id
                    }
                }
            }
            ''',
            op_name="JoinGame",
            variables={
                "gameId": self.game.id,
                "playerName": "John"
            }
        )
        self.assertResponseNoErrors(response)

    def test_leave_game(self):
        player = self.game.join("name")
        response = self.query(
            '''
            mutation LeaveGame($gameId: ID, $playerID: ID){
                leaveGame(gameId: $gameId, playerId: $playerID){
                    game {
                        id
                    }
                }
            }
            ''',
            op_name="LeaveGame",
            variables={
                "gameId": self.game.id,
                "playerID": player.id
            }
        )
        self.assertResponseNoErrors(response)

    def test_start_game(self):
        factories.PlayerFactory.create_batch(2, game=self.game)
        response = self.query(
            '''
                mutation StartGame($gameId: ID){
                    startGame(gameId: $gameId) {
                        game {
                            started
                        }
                    }
                }
            ''',
            op_name="StartGame",
            variables={
                "gameId": self.game.id,
            }
        )
        self.assertResponseNoErrors(response)
        self.game.save(update_fields={"started": True})

    @skip
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

    @skip
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
