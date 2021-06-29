from graphene_django.utils.testing import GraphQLTestCase

from codertheory.shiritori import models
from . import factories


class ShiritoriGraphQLTests(GraphQLTestCase):

    @classmethod
    def setUpTestData(cls):
        cls.game: models.ShiritoriGame = factories.GameFactory()

    def test_create_game(self):
        response = self.query(
            '''
            mutation ($private: Boolean){
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
            mutation ($gameId: ID, $playerName: String){
                joinGame(gameId: $gameId, playerName: $playerName){
                    player {
                        id
                    }
                }
            }
            ''',
            variables={
                "gameId": self.game.id,
                "playerName": "John"
            }
        )
        self.assertResponseNoErrors(response)

    def test_leave_game(self):
        player = self.game.join(self.game.id, "name")
        response = self.query(
            '''
            mutation ($playerID: ID){
                leaveGame(playerId: $playerID){
                    game {
                        id
                    }
                }
            }
            ''',
            variables={
                "playerID": player.id
            }
        )
        self.assertResponseNoErrors(response)

    def test_start_game(self):
        factories.PlayerFactory.create_batch(2, game=self.game)
        query_kwargs = dict(
            query='''
            mutation ($gameId: ID){
                startGame(gameId: $gameId) {
                    game {
                        started
                    }
                }
            }
        ''',
            variables={
                "gameId": self.game.id,
            }
        )
        response = self.query(**query_kwargs)
        self.assertResponseNoErrors(response)
        self.game.started = True
        self.game.save(update_fields=['started'])
        response = self.query(**query_kwargs)
        self.assertResponseHasErrors(response)

    def test_take_game_turn(self):
        player = factories.PlayerFactory(game=self.game)
        self.game.current_player = player
        self.game.last_word = "b"
        self.game.started = True
        self.game.save()
        query_kwargs = dict(
            query='''
                mutation ($gameID: ID,$word:String){
                    takeTurn(gameId: $gameID,word: $word){
                        score
                    }
                }
            ''',
            variables={
                "gameID": self.game.id,
                "word": "bar"
            }
        )
        response = self.query(**query_kwargs)
        self.assertResponseNoErrors(response)
        self.game.finished = True
        self.game.save()
        response = self.query(**query_kwargs)
        self.assertResponseHasErrors(response)
