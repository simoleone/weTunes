import frontend.models

class Queue:
    def __init__(self):
        self.playlist = None

    def generate_queue(self):
        if self.playlist is not None:
            return self.playlist
        
        unplayed_votes = Vote.objects.filter(played__exact = False)
        self.tracks = {}     # songid => set(self.users_voted)
        self.users = {}      # user => (last_vote_played_timestamp, set(songids_voted))
        self.playlist = []  # songid, in order
        self.timestamp = datetime.now()
        for v in unplayed_votes:
            self.process_vote(v)


        while len(self.tracks) > 0:
            # check if a track has more votes than the rest
            max_votes = 0
            fav_tracks = None
            for t in self.tracks:
                if fav_tracks is None or len(self.tracks[t]) > max_votes:
                    fav_tracks = set(t)
                    max_votes = len(self.tracks[t])
                elif len(self.tracks[t]) == max_votes:
                    fav_tracks.add(t)
            if fav_tracks is None or len(fav_tracks) == 0:
                # no tracks with a positive vote
                return self.playlist
            if len(fav_tracks) == 1:
                self.emit_track(fav_tracks.pop())
            else:
                # now find the user who's vote was played longest ago
                last_play_timestamp = None
                selected_track = None
                for t in fav_tracks:
                    for u in self.tracks[t]:
                        (user_timestamp, songids) = self.users[u]
                        if last_play_timestamp is None or user_timestamp < last_play_timestamp:
                            last_play_timestamp = user_timestamp
                            selected_track = t
                if selected_track is None:
                    return self.playlist
                else:
                    self.emit_track(selected_track)
        
        return self.playlist




    def emit_track(self, songid):
        self.playlist.append(songid)
        users_voted = self.tracks[songid]
        for u in users_voted:
            (last_play_timestamp, songids_voted) = self.users[u]
            songids_voted.discard(songid)
            # set the user's last play to be now (i.e. when this track will be played)
            self.users[u] = (self.timestamp, songids_voted)
        del tracks[songid]
        self.timestamp = self.timestamp + datetime.timedelta(minutes=3)




            




    def process_vote(self, v):
        if v.user in self.users:
            (last_play_timestamp, songids_voted_up) = self.users[v.user]
        else:
            songids_voted_up = set()
            try:
                last_play = Vote.objects.filter(played__exact = True, user__exact = v.user, upvote__exact = True).order_by('-updated')[0:1].get()
                last_play_timestamp = last_play.updated
            except DoesNotExist:
                last_play_timestamp = None
            self.users[v.user] = (last_play_timestamp, songids_voted_up)
        songids_voted_up.add(v.songid)
        if v.songid in self.tracks:
            self.tracks[v.songid].add(v.user)
        else
            self.tracks[v.songid] = set(v.user)

