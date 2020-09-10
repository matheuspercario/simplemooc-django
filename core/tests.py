from django.test import TestCase
from django.test.client import Client
from django.urls import reverse

# Create your tests here.
class HomeViewTest(TestCase):
    def test_home_status_code(self):
        print("Method: test_home_status_code")
        client = Client()
        response = client.get(reverse("core:home"))
        self.assertEqual(response.status_code, 200)

    def test_home_template_user(self):
        print("Method: test_home_template_user")
        client = Client()
        response = client.get(reverse("core:home"))
        self.assertTemplateUsed(response, "base.html")
        self.assertTemplateUsed(response, "home.html")
        # self.assertTemplateUsed(response, "not_used.html")
