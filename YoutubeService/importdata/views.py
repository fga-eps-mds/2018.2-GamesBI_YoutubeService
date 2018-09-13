import requests

from rest_framework.response import Response
from rest_framework.views import APIView

from .models import YouTubeSearch


class YouTubeView(APIView):
    '''
        View that calls IGDB API
        and return some relevant
        information about a game
        and filter for Null value
    '''
    def get(self, request, format=None):
        YouTubeSearch.objects.all().delete()
        header = {'user-key': 'AIzaSyDmDXP_gaB7cog4f0slbbdJ3RACsY5WQIw',
        'Accept': 'application/json'}
        url = 'https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=50&q={}&key={}'.format('PUBG', header['user-key'])
        data = requests.get(url)
        ndata = data.json()


        filtered_data = self.filter_data(ndata)
        self.save_youtube_search(filtered_data)
        '''
        games = YouTubeSearch.objects.all()

        for game in games:
            print('------------')
            print(game.id)
            print('------------')
        '''

        return Response(data=ndata)

    def get_video_data(self,id):
        YouTubeSearch.objects.all().delete()
        header = {'user-key': 'AIzaSyDmDXP_gaB7cog4f0slbbdJ3RACsY5WQIw',
        'Accept': 'application/json'}
        url = 'https://www.googleapis.com/youtube/v3/videos?part=statistics&id={}&key={}'.format('cAB2rWSW4w0', header['user-key'])
        data = requests.get(url)
        ndata = data.json()

        filtered_video_data = self.filter_video_data(ndata)
        self.save_youtube_search(filtered_video_data)

        return Response(data=ndata)

    def filter_data(self, gamedata):

        #print('aqui em cima: {}'.format(gamedata['items'][0]['id']['videoId']))
        for i in range(0,49):
            if 'items' in gamedata:
                if 'id' in gamedata['items'][i]:
                    if 'videoId' in gamedata['items'][i]['id']:
                        id = gamedata['items'][i]['id']['videoId']
                        print('\nid aqui: ', id)
                    else:
                        id = None
                else:
                    id = None
            else:
                id = None

            filtered_data = {
            'videoId': videoId,
            }

            return filtered_data


    def filter_video_data(self, videodata):

        if 'Unid' in videodata:

            if 'viewCount' in videodata['Unid'][0]:
                count_views=videodata['Unid'][0]['viewCount']
            else:
                count_views=None

            if 'likeCount' in videodata['Unid'][0]:
                count_likes=videodata['Unid'][0]['likeCount']
            else:
                count_views=None

            if 'dislikeCount' in videodata['Unid'][0]:
                count_dislikes=videodata['Unid'][0]['dislikeCount']

            if 'favoriteCount' in videodata['Unid'][0]:
                count_favorites=videodata['Unid'][0]['favoriteCount']

            if 'commentCount' in videodata['Unid'][0]:
                count_comments= videodata['Unid'][0]['commentCount']
            else:
                count_comments = None

        else:
            count_views=None
            count_likes=None
            count_dislikes=None
            count_favorites=None
            count_comments=None

            filtered_video_data = {
            'count_views': count_views,
            'count_likes': count_likes,
            'count_dislikes': count_dislikes,
            'count_favorites': count_favorites,
            'count_comments': count_comments,
            }

            return filtered_video_data


    def save_youtube_search(self, filtered_data, filtered_video_data):
        results = YouTubeSearch(
            id = filtered_data['id'],
            count_views = filtered_video_data['count_views'],
            count_likes = filtered_video_data['count_likes'],
            count_dislikes = filtered_video_data['count_dislikes'],
            count_favorites = filtered_video_data['count_favorites'],
            count_comments = filtered_video_data['count_comments'],
        )

        results.save()
        print('Id video: {}\n'.format(results.id))
