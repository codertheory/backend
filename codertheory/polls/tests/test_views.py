from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from . import factories


class PollViewTests(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.poll = factories.PollFactory()

    def test_list_polls(self):
        url = reverse("api:api_version_1:polls-list")
        response = self.client.get(url)
        self.assertEqual(len(response.data['results']), 1)

    def test_create_poll(self):
        url = reverse("api:api_version_1:polls-list")
        data = {
            "name": "Hello World",
            "options": [
                {
                    "option": "Option A"
                },
                {
                    "option": "Option B"
                }
            ]
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 201)

    def test_create_poll_missing_options(self):
        url = reverse("api:api_version_1:polls-list")
        data = {
            "name": "Yolo"
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertTrue("options" in response.data)

    def test_vote_poll(self):
        option = factories.PollOptionFactory(poll=self.poll)
        url = reverse("api:api_version_1:polls-vote", kwargs={"pk": self.poll.id})
        response = self.client.post(url, {"option": option.id})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(self.poll.total_vote_count, 1)
        self.assertEqual(option.vote_count, 1)
