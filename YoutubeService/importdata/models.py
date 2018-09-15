from django.db import models


class YouTubeSearch(models.Model):
    
    id = models.CharField(
        ('Video ID'),
        help_text=("Video ID"),
        max_length=100,
        primary_key=True
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