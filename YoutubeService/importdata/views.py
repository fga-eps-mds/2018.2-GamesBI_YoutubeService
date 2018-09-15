import requests
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import YouTubeSearch

#YouTubeSearch.objects.all().delete()

class YouTubeView(APIView):
    '''
        View that calls Youtube API
        and return some relevant
        information about a video
        and filter
    '''

    def get(self, request, format=None):

        igdb_header = {'Accept': 'application/json'}
        igdb_url = 'http://igdbweb:8000/api/get_igdb_games_list/name'
        igdb_data = requests.get(igdb_url, headers=igdb_header).json()
        
        i = 0
        YouTubeSearch.objects.all()
        for game in igdb_data:
            print('NOME DO JOGO: ' + game['name'])
            print("  ")
            print(" --------------------------------- ")
            print("  ")
            header = {'user-key': 'AIzaSyDmDXP_gaB7cog4f0slbbdJ3RACsY5WQIw',
            'Accept': 'application/json'}
            url = 'https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=50&q={}&key={}'.format(game['name'], header['user-key'])
            data = requests.get(url)
            ndata = data.json()
            filtered_data = self.filter_data(ndata)

            for id in filtered_data['list_id']:
                video_data = self.get_video(id)
                filter_data_video = self.filter_data_video(video_data)
                if filter_data_video:
                    self.save_youtube_search(filter_data_video)
                    print("Video de id " + str(id) + " salvo com sucesso!")
                    i = i + 1
                    print("Numero de videos baixados: " + str(i))
                    print(" ")

        return Response(data=igdb_data)


    def get_video(self, idvideo):
        YouTubeSearch.objects.all().delete()
        header = {'user-key': 'AIzaSyDmDXP_gaB7cog4f0slbbdJ3RACsY5WQIw',
        'Accept': 'application/json'}

        url = 'https://www.googleapis.com/youtube/v3/videos?part=statistics&id={}&key=AIzaSyDmDXP_gaB7cog4f0slbbdJ3RACsY5WQIw'.format(idvideo)
        data = requests.get(url)
        ndata = data.json()

        return ndata

    def filter_data(self, videodata):

        if 'regionCode' in videodata:
            regionCode = videodata['regionCode']
        else:
            regionCode = None

        items = []
        if 'items' in videodata:
            items = videodata['items']

        list_id = []
        for item in items:
            if 'id' in item:
                if 'videoId' in item['id']:
                    id = item['id']['videoId']
                    list_id.append(id)
                else:
                    id = None
            else:
                id = None

        filtered_data = {
            'list_id': list_id,
            'regionCode': regionCode
        }
        return filtered_data

    def filter_data_video(self, videodata):

        if 'items' in videodata:

            if 'id' in videodata['items']:
                id = videodata['items']['id']
            else:
                id = None

            if 'statistics' in videodata['items']:
                if 'viewCount' in videodata['items']['statistics']:
                    count_views = videodata['items']['statistics']['viewCount']
                else:
                    count_views = None

                if 'likeCount' in videodata['items']['statistics']:
                    count_likes = videodata['items']['statistics']['likeCount']
                else:
                    count_likes = None

                if 'dislikeCount' in videodata['items']['statistics']:
                    count_dislikes = videodata['items']['statistics']['dislikeCount']
                else:
                    count_dislikes = None

                if 'favoriteCount' in videodata['items']['statistics']:
                    count_favorites = videodata['items']['statistics']['favoriteCount']
                else:
                    count_favorites = None

                if 'commentCount' in videodata['items']['statistics']:
                    count_comments = videodata['items']['statistics']['commentCount']
                else:
                    count_comments = None
            else:
                id = None
                count_views = None
                count_likes = None
                count_dislikes = None
                count_favorites = None
                count_comments = None
        else:
            id = None
            count_views = None
            count_likes = None
            count_dislikes = None
            count_favorites = None
            count_comments = None

        filtered_data = {
            'id': id,
            'count_views': count_views,
            'count_likes': count_likes,
            'count_dislikes': count_dislikes,
            'count_favorites': count_favorites,
            'count_comments': count_comments
        }
        return filtered_data


    def save_youtube_search(self, filtered_data_video):

        results = YouTubeSearch(
            list_id = filtered_data_video['id'],
            #name = filtered_data['name'],
            count_views = filtered_data_video['count_views'],
            count_likes = filtered_data_video['count_likes'],
            count_dislikes = filtered_data_video['count_dislikes'],
            count_favorites = filtered_data_video['count_favorites'],
            count_comments = filtered_data_video['count_comments']
            #regionCode = filtered_data['regionCode']
        )

        results.save()
        #
        # print('-----RELACIONADO AO JOGO: {}---------\n'.format(game_name))
        # print('video id: {}\nviews: {}\nlikes: {}\ndislikes: {}\n'.format(results.list_id, results.count_views, results.count_likes, results.count_dislikes))
        # print('favorites: {}\ncomments: {}'.format(results.count_favorites, results.count_comments))
