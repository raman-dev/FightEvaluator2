from django.test import TestCase,SimpleTestCase
from http import HTTPStatus

# Create your tests here.
class UrlTests(SimpleTestCase):
    def test_index_exists(self):
        response = self.client.get("/v-index")
        self.assertEqual(response.status_code,HTTPStatus.OK)