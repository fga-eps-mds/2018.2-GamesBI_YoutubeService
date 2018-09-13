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



    def filter_data(self, gamedata, dataVD):
        
        list_id = []

        for i in range(50):
            if 'items' in gamedata:
                if 'id' in gamedata['items'][i]:
                    if 'videoId' in gamedata['items'][i]['id']:
                        id = gamedata['items'][i]['id']['videoId']
                        print('\nid aqui: ', id)
                        list_id.append(id)
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
        print('------------')        
        print(list_id)
        print('------------')
            

        if 'regionCode' in gamedata:
            regionCode = gamedata['regionCode']
        else:
            regionCode = None

        
        count_views = dataVD['items'][0]['statistics']['viewCount']
        count_likes = dataVD['items'][0]['statistics']['likeCount']
        count_dislikes = dataVD['items'][0]['statistics']['dislikeCount']
        count_favorites = dataVD['items'][0]['statistics']['favoriteCount']
        count_comments = dataVD['items'][0]['statistics']['commentCount']


        '''
        print('----------------\n', dataVD)
        if 'items' in dataVD:
            print('tem item')
            if 'statistics' in dataVD['items']:
                print('tem statistics\n')
                if 'viewCount' in dataVD['items']['statistics']:
                    count_views = dataVD['items']['statistics']['viewCount']
                    print('viewCount aqui: ', count_views)
                else:
                    count_views = None
            else:
                count_views = None
        else:
            count_views = None
        print('viewCount aqui: ', count_views)
        

        if 'likeCount' in statistics['items']:
            count_likes=statistics['items']['statistics']['likeCount']
        else:
            count_likes=None

        if 'dislikeCount' in statistics:
            count_dislikes=statistics['items']['statistics']['dislikeCount']
        else:
            count_dislikes = None

        if 'commentCount' in statistics:
            count_comments= statistics['items']['statistics']['commentCount']
        else:
            count_comments = None

        else:
            count_views=None
            count_likes=None
            count_dislikes=None
            count_favorites=None
            count_comments=None

            filtered_video_data = {
            
        '''   
        filtered_data = {
            'list_id': list_id,
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

            'regionCode': regionCode)
        
        return filtered_data

    def save_youtube_search(self, filtered_data):
        results = YouTubeSearch(
            id = filtered_data['list_id'],
            #name = filtered_data['name'],
            count_views = filtered_data['count_views'],
            count_likes = filtered_data['count_likes'],
            count_dislikes = filtered_data['count_dislikes'],
            count_favorites = filtered_data['count_favorites'],
            count_comments = filtered_data['count_comments'],
            regionCode = filtered_data['regionCode']
        )

        results.save()
        print('Id video: {}\n'.format(results.id))
        print('--------------\n')
        print('lista de id dos videos:{}\ncount views: {}\ncount likes: {}\ncount dislikes: {}\n'.format(results.id, results.count_views, results.count_likes, results.count_dislikes))
        print('count favorite: {}\ncount comments: {}'.format(results.count_favorites, results.count_comments))
        print('--------------\n')
