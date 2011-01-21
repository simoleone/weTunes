from django.db import models

# Create your models here.

class Vote(models.Model):
    user = models.CharField(max_length = 128)
    songid = models.IntegerField()
    updated = models.DateField(auto_now = True)
    played = models.BooleanField(default = False)
