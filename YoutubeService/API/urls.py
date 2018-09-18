from django.urls import include, path
from .views import GamesListView


urlpatterns = [
    path('get_youtube_games_list/',
         GamesListView.as_view(),
         name="get_youtube_games_Name_list"),
    # retorna uma lista com os dados  de todos os games salvos no banco de dados
]
