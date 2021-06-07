import json

from graphene_django.utils.testing import GraphQLTestCase

from . import factories


class PollGraphQLTests(GraphQLTestCase):

    @classmethod
    def setUpTestData(cls):
        cls.poll = factories.PollFactory()

    def test_list_polls(self):
        response = self.query(
            '''
            query {
               polls {
                    edges {
                        node {
                            id
                        }
                    }
               }

            }
            '''
        )
        self.assertResponseNoErrors(response)
        data = json.loads(response.content)['data']['polls']
        self.assertEqual(len(data), 1)
        self.assertEqual(data['edges'][0]['node']['id'], self.poll.id)

    def test_create_poll(self):
        response = self.query(
            '''
                mutation {
                    createPoll(name: "Yolo",description: "Bar",options: [
                        {
                            option: "A"
                        },
                        {
                            option: "B"
                        }
                    ]) {
                        poll {
                            id
                        }
                    }
                }
            '''
        )
        self.assertResponseNoErrors(response)
        self.assertEqual(response.status_code, 200)

    def test_create_poll_missing_options(self):
        response = self.query(
            '''
                mutation {
                    createPoll(name: "Yolo",description: "Bar",options: [
                        {
                            option: "A"
                        }
                    ]) {
                        poll {
                            id
                        }
                    }
                }

            '''
        )
        self.assertResponseHasErrors(response)

    def test_vote_poll(self):
        option = factories.PollOptionFactory(poll=self.poll)
        response = self.query(
            '''
                mutation VotePoll($pollID: ID,$optionID: ID) {
                    votePoll(optionId: $optionID, pollId: $pollID) {
                        vote {
                            __typename
                        }
                    }
                }

            ''',
            op_name="VotePoll",
            variables={'pollID': self.poll.id, 'optionID': option.id}
        )
        self.assertResponseNoErrors(response)
        self.assertEqual(self.poll.total_vote_count, 1)
        self.assertEqual(option.vote_count, 1)
