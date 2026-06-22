from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

# Create your tests here.


class HomePageTests(TestCase):
    def setUp(self):
        user = get_user_model().objects.create(username="Mike", password="testpass123")
        self.client.force_login(user)
        url = reverse("home")
        self.response = self.client.get(url)

    def test_url_exists_at_correct_location(self):
        """Ensure the homepage return an HTTP 200 status code."""
        self.assertEqual(self.response.status_code, 200)

    def test_homepage_template(self):
        """Ensure that home page is using the home.html template."""
        self.assertTemplateUsed(self.response, "home.html")
