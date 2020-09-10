from django.conf import settings
from django.core import mail
from django.test import TestCase
from django.test.client import Client
from django.urls import reverse
from model_mommy import mommy

from courses.models import Course

# Create your tests here.


class CouseManagerTestCase(TestCase):
    def setUp(self):
        print("setUp: Run once for every test method to setup clean data.")
        # MOMMY é um módulo especializado em testes, gera dados aleatórios automatiacmente
        self.course_django = mommy.make(
            "courses.Course", name="Python com Django", _quantity=10
        )
        self.course_dev = mommy.make(
            "courses.Course", name="Python para devs", _quantity=5
        )
        self.client = Client()

    def tearDown(self):
        Course.objects.all().delete()

    def test_course_search(self):
        print("Method: test_course_search")
        search = Course.objects.search("django")
        print(f"search[0]:{search[0].slug}")
        self.assertEqual(len(search), 10)
        search = Course.objects.search("dev")
        self.assertEqual(len(search), 5)
        search = Course.objects.search("python")
        self.assertEqual(len(search), 15)
