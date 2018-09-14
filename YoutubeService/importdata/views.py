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

        YouTubeSearch.objects.all().delete()
        header = {'user-key': 'AIzaSyDmDXP_gaB7cog4f0slbbdJ3RACsY5WQIw',
        'Accept': 'application/json'}
        url = 'https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=50&q={}&key={}'.format('GTAV', header['user-key'])
        data = requests.get(url)
        ndata = data.json()

        for i in range(49):
            filtered_data = self.filter_data(ndata)
            video_data = self.get_video(filtered_data['list_id'][i])
            filter_data_video = self.filter_data_video(video_data)
            if filter_data_video:
                self.save_youtube_search(filtered_data, filter_data_video, i)

        

        return Response(data=ndata)


    


       
    def get_video(self, idvideo):
        YouTubeSearch.objects.all().delete()
        header = {'user-key': 'AIzaSyDmDXP_gaB7cog4f0slbbdJ3RACsY5WQIw',
        'Accept': 'application/json'}

        url = 'https://www.googleapis.com/youtube/v3/videos?part=statistics&id={}&key=AIzaSyDmDXP_gaB7cog4f0slbbdJ3RACsY5WQIw'.format(idvideo)
        data = requests.get(url)
        ndata = data.json()

        return ndata

    def filter_data(self, videodata):

        list_id = []

        for i in range(50):
            if 'items' in videodata:
                if 'id' in videodata['items'][i]:
                    if 'videoId' in videodata['items'][i]['id']:
                        id = videodata['items'][i]['id']['videoId']
                        list_id.append(id)
                    else:
                        id = None
                else:
                    id = None
            else:
                id = None


        if 'regionCode' in videodata:
            regionCode = videodata['regionCode']
        else:
            regionCode = None

        filtered_data = {
            'list_id': list_id,
            'regionCode': regionCode
        }
        return filtered_data

    def filter_data_video(self, videodata):

        count_views = videodata['items'][0]['statistics']['viewCount']
        count_likes = videodata['items'][0]['statistics']['likeCount']
        count_dislikes = videodata['items'][0]['statistics']['dislikeCount']
        count_favorites = videodata['items'][0]['statistics']['favoriteCount']
        count_comments = videodata['items'][0]['statistics']['commentCount']

        '''
        print('----------------\n', videodata)
        if 'items' in videodata:
            print('tem item')
            if 'statistics' in videodata['items']:
                print('tem statistics\n')
                if 'viewCount' in videodata['items']['statistics']:
                    count_views = videodata['items']['statistics']['viewCount']
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
            count_comments=None

        '''

        filtered_data = {
                'count_views': count_views,
                'count_likes': count_likes,
                'count_dislikes': count_dislikes,
                'count_favorites': count_favorites,
                'count_comments': count_comments
        }
        return filtered_data


    def save_youtube_search(self, filtered_data, filtered_data_video, id):
        
        results = YouTubeSearch(
            list_id = filtered_data['list_id'][id],
            #name = filtered_data['name'],
            count_views = filtered_data_video['count_views'],
            count_likes = filtered_data_video['count_likes'],
            count_dislikes = filtered_data_video['count_dislikes'],
            count_favorites = filtered_data_video['count_favorites'],
            count_comments = filtered_data_video['count_comments']
            #regionCode = filtered_data['regionCode']
        )
        
        results.save()
        
        print('--------------\n')
        print('id do video:{}\ncount views: {}\ncount likes: {}\ncount dislikes: {}\n'.format(results.list_id, results.count_views, results.count_likes, results.count_dislikes))
        print('count favorite: {}\ncount comments: {}'.format(results.count_favorites, results.count_comments))
       
        