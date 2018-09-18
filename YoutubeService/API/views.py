import requests

from rest_framework.response import Response
from rest_framework.views import APIView

from YoutubeService.importdata.models import Game
from .serializers import GameSerializer


# Create your views here.
class GamesListView(APIView):
    serializer_class = GameSerializer

    def get(self, request, format=None):
        serializer = self.serializer_class(Game.objects.all(), many=True)
        return Response(serializer.data)
