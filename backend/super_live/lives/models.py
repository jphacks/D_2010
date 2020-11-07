#coding: utf-8
import datetime

from django.db import models
from django.utils import timezone

#liveのURLを管理
class Live(models.Model):
    liveName = models.CharField(verbose_name='liveName', max_length=100)
    liveUser = models.CharField(verbose_name='liveUser', max_length=100)
    liveId = models.CharField(verbose_name='liveId', max_length=100)
    pub_date = models.DateTimeField()

    def __str__(self):
        return self.liveId

#リアクションの管理
class Reactions(models.Model):
    live = models.ForeignKey(Live, on_delete=models.CASCADE)
    reaction = models.CharField(max_length=100)
    reactionCount = models.IntegerField(default=0)

    def __str__(self):
        return self.reaction

