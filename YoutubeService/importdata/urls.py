from django.urls import include, path
from .views import YouTubeView

urlpatterns = [
	path('get_youtube_search/', YouTubeView.as_view())
]
