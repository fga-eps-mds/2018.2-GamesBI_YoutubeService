from django.db import models

class Game(models.Model):
    id = models.IntegerField(
        ('Video ID'),
        help_text=("Id da Steam"),
        primary_key=True
    )
    name = models.CharField(
        ('Name'),
        help_text=("Name of game"),
        max_length=100,
        null=True
    )

    game_evaluation_chart = models.CharField(
        ('Game evaluation chart'),
        help_text=("Game evaluation chart"),
        max_length=100,
        null=True
    )

    Rating_reviews = models.CharField(
        ('Like or dislike in the game'),
        help_text=("Number of Like or dislike in the game"),
        max_length=100,
        null=True
    )

    def __str__(self):
        """
	    Returns the object as a string, the attribute that will represent
	    the object.
	    """
        return self.name
