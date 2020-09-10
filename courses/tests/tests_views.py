from django.conf import settings
from django.core import mail
from django.test import TestCase
from django.test.client import Client
from django.urls import reverse

from courses.models import Course

# Create your tests here.
class ContactCourseTestCase(TestCase):
    def setUp(self):
        print("setUp: Run once for every test method to setup clean data.")
        self.course = Course.objects.create(name="Django", slug="django")

    def tearDown(self):
        self.course.delete()

    def test_contact_form_error(self):
        print("Method: test_contact_form_error")
        client = Client()
        path = reverse("courses:details", args=[self.course.slug])
        data = {
            "name": "Matheus",
            "email": "",
            "message": "",
        }
        response = client.post(path, data)
        self.assertFormError(response, "form", "email", "Este campo é obrigatório.")
        self.assertFormError(response, "form", "message", "Este campo é obrigatório.")

    def test_contact_form_success(self):
        print("Method: test_contact_form_success")
        client = Client()
        path = reverse("courses:details", args=[self.course.slug])
        data = {
            "name": "Matheus",
            "email": "admin@admin.com",
            "message": "Olá",
        }
        response = client.post(path, data)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, [settings.CONTACT_EMAIL])
