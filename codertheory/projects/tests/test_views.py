from unittest import skip

from django import urls
from django.test import TestCase

from codertheory.users.tests import factories


class ProjectsViewsTests(TestCase):

    def setUp(self) -> None:
        token = factories.DRFTokenFactory()
        self.client.force_login(token.user)

    @skip("Figure out how to properly encode the signature to test")
    def test_webhook_view(self):
        url = urls.reverse("projects:github")
        data = {
            "var1": 1
        }
        signature = "sha256=842AFA6CD656C63B9E058C5A74A467FEC4744E9773C9D89EEC51D683E4D83795"
        response = self.client.post(url, data, content_type="application/json",
                                    HTTP_X_HUB_SIGNATURE_256=signature)
        self.assertEquals(response.status_code, 200)
