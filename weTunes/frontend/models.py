from django.db import models

# Create your models here.

class Vote(models.Model):
    block = models.ForeignKey('Block')
    user = models.CharField(max_length = 128)
    created = models.DateField(auto_now = True)
    
class Block(models.Model):
    length = models.IntegerField()

class Track(models.Model):
    block = models.ForeignKey('Block')
    filename = models.CharField(max_length = 1024)
    track_number = models.IntegerField()
