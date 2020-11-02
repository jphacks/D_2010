from django.db import models

#liveのURLを管理
class Live(models.Model):
    liveURL = models.CharField(max_length=2000)
    pub_date = models.DateFiels()

    def __str__(self):
        return self.LiveURL

#リアクションの管理
class Reaction(models.Model):
    live = models.Foreignkey(Live, on_delete=models.CASCADE)
    reaction = models.IntegerField(default=0)

    def __str__(self):
        return self.reaction
