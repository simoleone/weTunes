from django.db import models
from datetime import datetime, timedelta
from frontend.lib.mpc import MPC

class Vote(models.Model):
    block = models.ForeignKey('Block')
    user = models.CharField(max_length = 128)
    created = models.DateTimeField(auto_now_add = True)
    
class Block(models.Model):
    length = models.IntegerField()

    def priority_score(self, when = None):
        # score = sum(wait time) / length
        if when is None:
            when = datetime.now()
        score = timedelta()
        votes = self.vote_set.all()
        for v in votes:
            score += (when - v.created)
        self.priority = score.total_seconds() / float(self.length)
        return self.priority

    def update_length(self):
        tracks = self.track_set.all()
        time = 0
        for t in tracks:
            time += int(MPC().find('file', t.filename)[0]['time'])
        self.length = time
        self.save()


class Track(models.Model):
    # TODO: make track removals cascade to blocks and votes
    block = models.ForeignKey('Block')
    filename = models.CharField(max_length = 1024)
    track_number = models.IntegerField()
    playlist_id = models.IntegerField(null = True)

    def delete(self):
        super.delete()

        # ensure that empty blocks are cleaned up
        if self.block.track_set.all().count() == 0:
            self.block.vote_set.delete()
            self.block.delete()
