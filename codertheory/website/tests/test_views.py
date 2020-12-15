from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class GeneralViewsTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_superuser("foobar@baz.com", "passwordispassword")
        return cls

    def test_home_view(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_about_us_view(self):
        path = reverse("website:about-us-view")
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['staff_members'], [repr(self.user)])

    def test_privacy_policy_view(self):
        path = reverse("website:privacy-policy-view")
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200)
