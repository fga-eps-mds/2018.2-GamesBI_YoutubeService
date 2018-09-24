from django.db import models

class Game(models.Model):

    id = models.IntegerField(
        ('Youtube ID'),
        help_text=("Id of Youtube"),
        primary_key=True
    )

    name = models.CharField(
        ('Name'),
        help_text=("Name of game"),
        max_length=100,
        null=True
    )

    count_videos = models.IntegerField(
        ('count_videos'),
        help_text=('Numbers of videos in game'),
        null=True
    )

    count_views = models.IntegerField(
        ('count_views'),
        help_text=('Numbers of video views'),
        null=True
    )

    count_likes = models.IntegerField(
        ('count_likes'),
        help_text=("Number of likes"),
        null=True
    )

    count_dislikes = models.IntegerField(
        ('count_dislikes'),
        help_text=("Number of dislikes"),
        null=True
    )

    count_comments = models.IntegerField(
        ('count_comment'),
        help_text=('Number of comment'),
        null=True
    )

    count_favorites = models.IntegerField(
        ('count_favorites'),
        help_text=("Number favorites of video"),
        null=True
    )

    def __str__(self):
        """
            Returns the object as a string, the attribute that will represent
            the object.
        """
        return self.name
