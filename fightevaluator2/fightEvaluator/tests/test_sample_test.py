from django.test import TestCase,SimpleTestCase
from http import HTTPStatus

from ..models import FightEvent
# Create your tests here.
class UrlTests(SimpleTestCase):
    def test_index_exists(self):
        response = self.client.get("/v-index")
        self.assertEqual(response.status_code,HTTPStatus.OK)


class FightEventTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # return super().setUpTestData()
        cls.event = FightEvent.objects.create(
            title="UFC Sample Event",
            date="2026-01-01"
            )
        