from frontend.models import Vote, Block, Track
from frontend.lib.mpc import MPC
from datetime import datetime, timedelta

class Queue:
    def __init__(self):
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
        playlist = MPC().playlistid()
    
        #trim the head of the list
        while len(playlist) > 0 and playlist[0]['id'] != queue[0].playlist_id:
            MPC().deleteid(playlist[0]['id'])
            playlist.pop(0)

        #XXX FIXME TODO finish this

            

#    def save_queue(self):
#        self.get_queue()
#        # clear everything from MPC's queue except the current song
#        current_song = MPC().currentsong()
#        current_playlist = MPC().playlistid()
#        if not current_song or 'file' not in current_song:
#            current_song = {'file': None}
#        for s in current_playlist:
#            if s['file'] != current_song['file']:
#                MPC().deleteid(s['id'])
#
#        for filename in self.queue:
#            MPC().findadd('file', filename)
#
#    def update_played(self):
#        current_playlist = MPC().playlistinfo()
#        current_song = MPC().currentsong()
#        if not current_song or 'file' not in current_song:
#            return
#        played_songs = []
#        for s in current_playlist:
#            played_songs.append(s)
#            if s['file'] == current_song['file']:
#                # we've reached the currently-playing song
#                self.mark_played(played_songs)
#                return
#
#    def mark_played(self, played_songs):
#        for s in played_songs:
#            Vote.objects.filter(played__exact = False, filename__exact = s['file']).update(played = True)

