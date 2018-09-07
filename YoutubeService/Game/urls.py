from django.urls import include, path
from .views import SteamView

urlpatterns = [
    # path('get_steam_games_list/', SteamView.as_view(), name="get_steam_games"),
    path('get_steam_games_list/', SteamView.as_view())
]
