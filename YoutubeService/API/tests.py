from django.test import TestCase
from model_mommy import mommy
from YoutubeService.importdata.models import Game
from rest_framework.test import APITestCase, URLPatternsTestCase
from django.urls import include, path, reverse
from rest_framework import status

# Create your tests here.
class EndpointTestCase(APITestCase, URLPatternsTestCase):

    urlpatterns= [
        path('api/', include('YoutubeService.API.urls'))
    ]

    def setUp(self):

        self.Game_yotube = mommy.make(
            Game,
            id = 0,
            name = "teste",
            count_views = 0,
            count_likes = 0,
        )

        self.youtube_endpoint = reverse('get_youtube_games_Name_list')

    def tearDown(self):

        Game.objects.all().delete()

    def test_status_youtube_endpoint(self):

        response = self.client.get(self.youtube_endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_response_youtube_endpoint(self):

        response = self.client.get(self.youtube_endpoint,format = 'json')

        for data in response.data:
            self.assertNotEqual(data['id'], None)
            self.assertNotEqual(data['name'], None)
