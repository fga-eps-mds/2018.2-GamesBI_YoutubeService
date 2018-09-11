from .models import YouTubeView
from rest_framework import serializers

class GameSerializer(serializers.ModelSerializer):

	class Meta:
		model = YouTubeSearch
		#fields = '__all__'
		fields = ('id',	'regionCode')
