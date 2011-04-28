from frontend.models import Vote, Block, Track, StateVar
from frontend.lib.mpc import MPC
from datetime import datetime

class Queue:

    """Sync the current calculated queue to mpd's queue"""
    def save_queue(self):
        queue = self.compute_queue(True)

        for i in range(len(queue)):
            if queue[i].playlist_id is not None:
                MPC().moveid(queue[i].playlist_id, i)
            else:
                queue[i].playlist_id = MPC().addid(queue[i].filename, i)
                queue[i].save()

        return queue

    """Compute the current queue based on votes for blocks and
       currently playing block.

       returns a list of Tracks
    """
    def compute_queue(self, update=False):
        # 1. determine current block
        # 2. calculate scores for all other blocks
        # 3. output tracks in order: current block, then remaining blocks by descending score

        play_queue = []
        blocks_to_score = []
        if update:
            cursong_id = self.__clean_playlist()
        else:
            status = MPC().status()
            if status.has_key('songid'):
                cursong_id = status['songid']
            else:
                cursong_id = None

        if cursong_id == None:
            # play queue has never been saved to mpd
            # calculate scores for all blocks
            blocks_to_score = list(Block.objects.all())
        else:
            # add tracks in the current block to the queue
            curblock = Track.objects.filter(playlist_id = cursong_id)[0].block
            curblock_tracks = curblock.track_set.all().order_by('track_number')
            play_queue += list(curblock.track_set.all().order_by('track_number'))
            # and score the rest...
            blocks_to_score = list(Block.objects.exclude(id = curblock.id))

        # sort them by score
        d = datetime.now()
        blocks_to_score.sort(key=lambda x : Block.priority_score(x, d))

        # add remaining tracks to the queue
        for b in blocks_to_score:
            play_queue += list(b.track_set.all().order_by('track_number'))

        return play_queue

    """Remove any already played songs from playlist and database
       returns playlist id of currently playing song or None
    """
    def __clean_playlist(self):
        status = MPC().status()
        plinfo = MPC().playlistinfo()
        playtime = int(MPC().stats()['playtime'])
        try:
            old_playtime = StateVar.objects.get(key='playtime')
        except StateVar.DoesNotExist: # fresh db?
            old_playtime = StateVar(key='playtime', val=str(playtime))
            old_playtime.save()

        if status['playlistlength'] == '0':
            # no queue has been synced to mpd yet
            return None
        elif not status.has_key('songid'):
            # either play has not started, or the play queue was finished
            #  if play hasn't started, we'll return the first song
            if playtime <= int(old_playtime.val):
                return plinfo[0]['id']
            #  otherwise, we'll nuke the mpd queue and return None
            else:
                status['songid'] = None


        # delete everything up to the current song
        for song in plinfo:
            songid = song['id']
            if songid == status['songid']:
                break
            MPC().deleteid(songid)
            Track.objects.filter(playlist_id = songid).delete()

        old_playtime.val = str(playtime)
        old_playtime.save()
        return status['songid']
