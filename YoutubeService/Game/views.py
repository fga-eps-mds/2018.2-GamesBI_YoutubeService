import requests

from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Game
from .serializers import GameSerializer


class SteamView(APIView):
    '''
        View that calls IGDB API
        and return some relevant
        information about a game
        and filter for Null value
    '''
    def get(self, request, format=None):
        Game.objects.all().delete()
        header = {'user-key': 'ddedabe2e2f2271bd81da64857d19a52',
        'Accept': 'application/json'}
        url = 'https://api-endpoint.igdb.com/games/?fields=id,name,hypes,popularity,aggregated_rating,time_to_beat,genres&filter[rating][gte]=60&order=popularity:desc&limit=50&offset=0'
        data = requests.get(url, headers=header)
        ndata = data.json()

        for gamedata in ndata:
            filtered_data = self.filter_data(gamedata)
            self.save_game(filtered_data)

        games = Game.objects.all()
        for game in games:
            print('------------')
            print(game.id)
            print(game.name)
            print('------------')

        return Response(data=ndata)

    def filter_data(self, gamedata):
        if 'id' in gamedata:
            id = gamedata['id']
        else:
            id = None
        if 'name' in gamedata:
            name = gamedata['name']
        else:
            name = None

        filtered_data = {
            'id': id,
            'name': name
        }
        return filtered_data

    def save_game(self, filtered_data):
        new_game = Game(
            id = filtered_data['id'],
            name = filtered_data['name']
        )
        new_game.save()
        print('o jogo salvou ' + new_game.name)
