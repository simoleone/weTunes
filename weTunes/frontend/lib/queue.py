from frontend.models import Vote
from frontend.lib.mpc import MPC
from datetime import datetime, timedelta

class Queue:
    def __init__(self):
        self.queue = None
        self.playlist = None

    def get_playlist(self):
        self.get_queue()
        return self.playlist

    def get_queue(self):
        if self.queue is not None:
            return self.queue
        
        unplayed_votes = Vote.objects.filter(played__exact = False)
        self.tracks = {}     # filename => set(self.users_voted)
        self.users = {}      # user => (last_vote_played_timestamp, set(filenames_voted))
        self.queue = []  # filename, in order
        self.playlist = []
        self.timestamp = datetime.now()
        for v in unplayed_votes:
            self.analyze_vote(v)

        while len(self.tracks) > 0:
            # check if a track has more votes than the rest
            max_votes = 0
            fav_tracks = None
            for t in self.tracks:
                if fav_tracks is None or len(self.tracks[t]) > max_votes:
                    fav_tracks = set()
                    fav_tracks.add(t)
                    max_votes = len(self.tracks[t])
                elif len(self.tracks[t]) == max_votes:
                    fav_tracks.add(t)
            if fav_tracks is None or len(fav_tracks) == 0:
                # no tracks with a positive vote
                return self.queue
            elif len(fav_tracks) == 1:
                self.emit_track(fav_tracks.pop())
            else:
                # now find the user who's vote was played longest ago
                last_play_timestamp = None
                selected_track = None
                for t in fav_tracks:
                    for u in self.tracks[t]:
                        (user_timestamp, filenamess) = self.users[u]
                        if last_play_timestamp is None or user_timestamp < last_play_timestamp:
                            last_play_timestamp = user_timestamp
                            selected_track = t
                if selected_track is None:
                    return self.queue
                else:
                    self.emit_track(selected_track)
        
        return self.queue

    def emit_track(self, filename):
        users_voted = self.tracks[filename]
        self.queue.append(filename)
        try:
            song = MPC().search('file', filename)[0]
            song['votes'] = len(users_voted)
            song['voters'] = users_voted
            self.playlist.append(song)
        except IndexError:
            print "Could not find file %s" % filename

        for u in users_voted:
            (last_play_timestamp, filenames_voted) = self.users[u]
            filenames_voted.discard(filename)
            # set the user's last play to be now (i.e. when this track will be played)
            self.users[u] = (self.timestamp, filenames_voted)
        del self.tracks[filename]
        self.timestamp = self.timestamp + timedelta(minutes=3)

    def analyze_vote(self, v):
        if v.user in self.users:
            (last_play_timestamp, filenames_voted_up) = self.users[v.user]
        else:
            filenames_voted_up = set()
            try:
                last_play = Vote.objects.filter(played__exact = True, user__exact = v.user).order_by('-updated')[0:1].get()
                last_play_timestamp = last_play.updated
            except Vote.DoesNotExist:
                last_play_timestamp = None
            self.users[v.user] = (last_play_timestamp, filenames_voted_up)
        filenames_voted_up.add(v.filename)
        if v.filename not in self.tracks:
            self.tracks[v.filename] = set()
        self.tracks[v.filename].add(v.user)

    def save_queue(self):
        self.get_queue()
        MPC().clear()
        for filename in self.queue:
            MPC().findadd('file', filename)
