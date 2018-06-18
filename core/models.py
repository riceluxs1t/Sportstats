from django.db import models


class RawMatch(models.Model):
    date = models.DateField()
    home_team = models.CharField(max_length=128)
    away_team = models.CharField(max_length=128)
    home_team_score = models.IntegerField()
    away_team_score = models.IntegerField()
    location = models.CharField(max_length=128)
    match_type = models.CharField(max_length=128)
    home_advantage = models.BooleanField(default=False)

    home_team_rating = models.IntegerField()
    away_team_rating = models.IntegerField()
    home_team_rating_change = models.IntegerField()
    away_team_rating_change = models.IntegerField()
    home_team_rank = models.IntegerField()
    away_team_rank = models.IntegerField()
    home_team_rank_change = models.IntegerField()
    away_team_rank_change = models.IntegerField()
