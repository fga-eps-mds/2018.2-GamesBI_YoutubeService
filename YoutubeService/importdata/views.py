import requests
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import YouTubeSearch

class YouTubeView(APIView):
    '''
        View that calls Youtube API
        and return some relevant
        information about a video
        and filter
    '''

    def get(self, request, format=None):

        YouTubeSearch.objects.all()
        igdb_game_list=self.get_igdb_game_list();
        game_number=int(0)
        total_videos=int(0)
        
        for game in igdb_game_list:
            search_on_youtube=self.get_search_result(game['name'])
            list_id=self.filter_data(search_on_youtube)
            game_number+=1

            for id in range(len(list_id)):
                video_data=self.get_video_data(list_id[id])
                filter_video_data = self.filter_data_video(video_data)
                total_videos+=1
                
                if filter_video_data:
                    results=self.save_youtube_search(list_id[id], filter_video_data)
                    
                    print('\n\nTOTAL DE VIDEOS ENCONTRADOS: {}\n-----RELACIONADO AO JOGO (Nº {}): {}----'.format(total_videos, game_number, game['name']))
                    print('                  (RESULTADO: {} VIDEOS)\n'.format(len(list_id)))
                    print('video id: {}\nviews: {}\nlikes: {}\ndislikes: {}'.format(results.id, results.count_views, results.count_likes, results.count_dislikes))
                    print('favorites: {}\ncomments: {}\n\nvideo nº: {}\n'.format(results.count_favorites, results.count_comments, id+1))
                    
        return Response(data=filter_video_data)

    
    def get_igdb_game_list(self):
        header={'Accept': 'application/json'}
        igdb_url='http://igdbweb:8000/api/get_igdb_games_list/name'
        igdb_game_list=requests.get(igdb_url, headers=header).json()

        return igdb_game_list

    def get_search_result(self, game_name):
        header={'Accept':'application/json'}
        key='AIzaSyDmDXP_gaB7cog4f0slbbdJ3RACsY5WQIw'
        url='https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=50&q={}&key={}'.format(game_name, key)
        result=requests.get(url).json()

        return result
        
    def filter_data(self, youtube_results):

        items=[]
        if 'items' in youtube_results:
            items=youtube_results['items']
        
        list_id=[]
        for item in items:
            if 'id' in item:
                if 'videoId' in item['id']:
                    id=item['id']['videoId']
                    list_id.append(id)
                else:
                    id= None
            else:
                id=None

        return list_id

    def get_video_data(self, idvideo):
        YouTubeSearch.objects.all().delete()
        header = {'user-key': 'AIzaSyDmDXP_gaB7cog4f0slbbdJ3RACsY5WQIw',
        'Accept': 'application/json'}
        url = 'https://www.googleapis.com/youtube/v3/videos?part=statistics&id={}&key=AIzaSyDmDXP_gaB7cog4f0slbbdJ3RACsY5WQIw'.format(idvideo)
        video_data = requests.get(url).json()

        return video_data

    
    def filter_data_video(self, video_data):

        if 'items' in video_data:
            items=video_data['items']

            for item in items:

                if 'statistics' in item:
                    if 'viewCount' in item['statistics']:
                        count_views = item['statistics']['viewCount']
                    else:
                        count_views = None

                    if 'likeCount' in item['statistics']:
                        count_likes = item['statistics']['likeCount']
                    else:
                        count_likes = None

                    if 'dislikeCount' in item['statistics']:
                        count_dislikes = item['statistics']['dislikeCount']
                    else:
                        count_dislikes = None

                    if 'favoriteCount' in item['statistics']:
                        count_favorites = item['statistics']['favoriteCount']
                    else:
                        count_favorites = None

                    if 'commentCount' in item['statistics']:
                        count_comments = item['statistics']['commentCount']
                    else:
                        count_comments = None
                else:
                    count_views = None
                    count_likes = None
                    count_dislikes = None
                    count_favorites = None
                    count_comments = None
        else:
            count_views = None
            count_likes = None
            count_dislikes = None
            count_favorites = None
            count_comments = None
        
        filtered_data_video = {
            'count_views': count_views,
            'count_likes': count_likes,
            'count_dislikes': count_dislikes,
            'count_favorites': count_favorites,
            'count_comments': count_comments
        }
        return filtered_data_video


    def save_youtube_search(self, video_id, filtered_data_video):

        results=YouTubeSearch(
            id=video_id,
            count_views=filtered_data_video['count_views'],
            count_likes=filtered_data_video['count_likes'],
            count_dislikes=filtered_data_video['count_dislikes'],
            count_favorites=filtered_data_video['count_favorites'],
            count_comments=filtered_data_video['count_comments']
        )

        results.save()
        
        return results