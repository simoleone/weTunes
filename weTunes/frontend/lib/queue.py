from frontend.models import Vote, Block, Track
from frontend.lib.mpc import MPC
from datetime import datetime, timedelta

class Queue:
    def __init__(self):
        self.compute_queue()
        pass

    def compute_queue(self):
        queue = []
        # start with the current block
        current_song_id = MPC().currentsong()['id']
        current_track = Track.objects.get(playlist_id = current_song_id)
        queue.append(current_track)
        tracks_in_block = list(Track.objects.filter(block = current_track.block, track_number__gt = current_track.track_number).order_by('track_number'))
        queue += tracks_in_block

        blocks = sorted(list(Block.objects.exclude(id = current_track.block)), Block.priority_score)
        for b in blocks:
            tracks_in_block = list(Track.objects.filter(block = b).order_by('track_number'))
            queue += tracks_in_block
        print queue
        return queue

    def save_queue(self):
        queue = self.compute_queue()

        validids = set()
    
        for i in range(len(queue)):
            if queue[i].playlist_id is not None:
                MPC().moveid(queue[i].playlist_id, i)
            else:
                queue[i].playlist_id = MPC().addid(queue[i].filename, i)
                queue[i].save()
            validids.add(queue[i].playlist_id)

        playlist = MPC().playlistid()
        for track in playlist:
            if track['id'] not in validids:
                MPC().deleteid(track['id'])
                t = Track.objects.get(playlist_id = track['id'])
                blockid = t.block
                t.delete()
                if Track.objects.count(block = blockid) == 0:
                    Vote.objects.delete(block = blockid)
                    Block.objects.delete(id = blockid)
