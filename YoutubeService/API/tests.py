from django.test import TestCase
from model_mommy import mommy
from Youtubservice.importdata.model import Game
from rest_framework.test import APITesteCase, URLPatternsTestCase
from django.urls import include, path, reverse
from rest_framework import status

# Create your tests here.
class EndpointsTestCase (APITesteCadse, URLPatternsTestCase):

    urlpatterns= [
        path('api/', include('Youtubservice.API.urls'))
    ]

    def setUP(self):
        self.Game = mommy.make(
            Game,
            id = 0,
            name = "teste",
            count_views = 0,
            count_likes = 0,
        )
        self.youtube_endpoint = reverse('get_igdb_games_id_youtube_list')
#       self.name_endpoint = reverse('get_youtube_games_Name_list')
    def tearDown(self):
        Game.objects.all().delete()

    def test_status_youtube_endpoint(self):
        response = self.client.get(self.youtube_endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_response_youtube_endpoint(self):

        response = self.client.get(self.youtube_endpoint,format = 'json')
        self.assertEqual(Game.objects.all().count(), 1)

        for jogo in response.data:
            self.assertNotEqual(response.data['nome'],None)
        
