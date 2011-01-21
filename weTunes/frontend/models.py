from django.db import models
from datetime import datetime, timedelta
from frontend.lib.mpc import MPC

# Create your models here.

class Vote(models.Model):
    block = models.ForeignKey('Block')
    user = models.CharField(max_length = 128)
    created = models.DateField(auto_now_add = True)
    
class Block(models.Model):
    length = models.IntegerField()

    def priority_score(self, when = None):
        if self.priority is not None:
            return self.priority
        if self.length == 0:
            return 0
        # score = sum(wait time) / length
        if when is None:
            when = datetime.now()
        score = timedelta.timedelta()
        votes = Vote.objects.filter(block__exact = self)
        for v in votes:
            score += (when - v.created)
        self.priority = int(score) / float(self.length)
        return self.priority

    def update_length(self):
        tracks = Track.objects.filter(block__exact = self)
        time = 0
        for t in tracks:
            time += int(MPC().find('file', t.filename)[0]['time'])
        self.length = time
        self.save()


class Track(models.Model):
    block = models.ForeignKey('Block')
    filename = models.CharField(max_length = 1024)
    track_number = models.IntegerField()
    playlist_id = models.IntegerField(null = True)
