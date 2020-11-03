import datetime

from django.db import models
from django.utils import timezone

#liveのURLを管理
class Live(models.Model):
    liveName = models.CharField(max_length=100)
    liveId = models.CharField(max_length=100)
    pub_date = models.DateTimeField()

    def __str__(self):
        return self.LiveId

#リアクションの管理
class Reactions(models.Model):
    live = models.ForeignKey(Live, on_delete=models.CASCADE)
    reaction = models.CharField(max_length=100)

    def __str__(self):
        return self.reaction
#リアクションの数を管理
class ReactionCount(models.Model):
    happy = models.IntegerField(default=0)

    def __str__(self):
        return self.happy