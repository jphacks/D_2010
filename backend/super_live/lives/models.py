from django.db import models

#liveのURLを管理
class Live(models.Model):
    liveId = models.CharField(max_length=100)
    pub_date = models.DateFiels()

    def __str__(self):
        return self.LiveId

#リアクションの管理
class Reactions(models.Model):
    live = models.Foreignkey(Live, on_delete=models.CASCADE)
    reaction = models.CharField(max_length=100)

    def __str__(self):
        return self.reaction

class ReactionCount(models.Model):
    happy = models.IntegerField(default=0)

    def __str __(self):
        return self.happy