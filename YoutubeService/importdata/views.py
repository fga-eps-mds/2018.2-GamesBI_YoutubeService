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

        igdb_game_list = self.get_igdb_game_list()
        YouTubeSearch.objects.all()
        qtd_jogos = 0
        qtd_videos=0
        for game in igdb_game_list:
            
            statistics = {
                'name': game['name''],
                'count_views': 0,
                'count_likes': 0,
                'count_dislikes': 0,
                'count_favorites': 0,
                'count_comments': 0
            }

            search_on_youtube = self.get_search_result(statistics['name'])
            list_id = self.filter_data(search_on_youtube)

            for id in list_id:
                video_data = self.get_video_data(id)
                filter_video_data = self.filter_data_video(video_data)
                statistics['count_views'] = statistics['count_views'] + filter_video_data['count_views']
                statistics['count_likes'] = statistics['count_likes'] + filter_video_data['count_likes']
                statistics['count_dislikes'] = statistics['count_dislikes'] + filter_video_data['count_dislikes']
                statistics['count_favorites'] = statistics['count_favorites'] + filter_video_data['count_favorites']
                statistics['count_comments'] = statistics['count_comments'] + filter_video_data['count_comments']
                qtd_videos+=1
                print("Quantidade de jogos salvos: {} / Quantidade de videos requisitados: {}" .format(qtd_jogos, qtd_videos))
                print("------------------------------------------------------------------------")
                print("Video: {} requisitado com sucesso! - Jogo atual: {}\n" .format(id, statistics['name']) )
                self.do_log_game(statistics)

            save = self.save_youtube_search(statistics)
            if save:
                print("JOGO " + statistics['name'] + " SALVO COM SUCESSO!\n\n")
                qtd_jogos+=1

        return Response(data=igdb_game_list)

    def do_log_game(self, game_info):
        print("DADOS DO JOGO ATUAL: ")
        print("Nome: {}" .format(game_info['name']))
        print("Views: {}" .format(game_info['count_views']))
        print("Likes: {}" .format(game_info['count_likes']))
        print("Dislikes: {}" .format(game_info['count_dislikes']))
        print("Favorites: {}" .format(game_info['count_favorites']))
        print("Comments: {}\n\n\n" .format(game_info['count_comments']))


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


    def get_video_data(self, idvideo):
        YouTubeSearch.objects.all().delete()
        header = {'Accept': 'application/json'}
        key = 'AIzaSyDmDXP_gaB7cog4f0slbbdJ3RACsY5WQIw'
        url = 'https://www.googleapis.com/youtube/v3/videos?part=statistics&id={}&key={}'.format(idvideo, key)
        video_data = requests.get(url).json()
        return video_data


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


    def filter_data_video(self, video_data):

        if 'items' in video_data:
            items=video_data['items']

            for item in items:

                if 'statistics' in item:
                    if 'viewCount' in item['statistics']:
                        count_views = item['statistics']['viewCount']
                    else:
                        count_views = 0

                    if 'likeCount' in item['statistics']:
                        count_likes = item['statistics']['likeCount']
                    else:
                        count_likes = 0

                    if 'dislikeCount' in item['statistics']:
                        count_dislikes = item['statistics']['dislikeCount']
                    else:
                        count_dislikes = 0

                    if 'favoriteCount' in item['statistics']:
                        count_favorites = item['statistics']['favoriteCount']
                    else:
                        count_favorites = 0

                    if 'commentCount' in item['statistics']:
                        count_comments = item['statistics']['commentCount']
                    else:
                        count_comments = 0
                else:
                    count_views = 0
                    count_likes = 0
                    count_dislikes = 0
                    count_favorites = 0
                    count_comments = 0
        else:
            count_views = 0
            count_likes = 0
            count_dislikes = 0
            count_favorites = 0
            count_comments = 0

        filtered_data_video = {
            'count_views': int(count_views),
            'count_likes': int(count_likes),
            'count_dislikes': int(count_dislikes),
            'count_favorites': int(count_favorites),
            'count_comments': int(count_comments)
        }
        return filtered_data_video


    def save_youtube_search(self, statistics):
        results=YouTubeSearch(
            name=statistics['name'],
            count_views=statistics['count_views'],
            count_likes=statistics['count_likes'],
            count_dislikes=statistics['count_dislikes'],
            count_favorites=statistics['count_favorites'],
            count_comments=statistics['count_comments']
        )
        results.save()
        return results
