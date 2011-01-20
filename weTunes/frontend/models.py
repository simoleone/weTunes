from django.db import models

# Create your models here.

class Vote(models.Model):
    user = models.CharField(max_length = 128)
    songid = models.IntegerField()
    upvote = models.BooleanField()
    updated = models.DateField(auto_now = True)

