from django.test import SimpleTestCase
from django.urls import reverse

# Create your tests here.


class HomePageTests(SimpleTestCase):
    def setUp(self):
        url = reverse("home")
        self.response = self.client.get(url)

    def test_url_exists_at_correct_location(self):
        """Ensure the homepage return an HTTP 200 status code."""
        self.assertEqual(self.response.status_code, 200)

    def test_homepage_template(self):
        """Ensure that home page is using the home.html template."""
        self.assertTemplateUsed(self.response, "home.html")
