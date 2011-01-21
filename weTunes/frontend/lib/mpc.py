from mpd import MPDClient, CommandError
from socket import error as SocketError

from django.conf import settings

"An exception class for errors in MPC"
class MPCError(Exception):
    def __init__(self, value):
        self.parameter = value
    def __str__(self):
        return repr(self.parameter)

"""A class to easily interface with the running MPD.
   See also python-mpd. This is just a really thin wrapper.
"""
class MPC:
    __client = None

    "Create an mpdclient using default connection"
    def __init__(self):
        # instantiate the client if necessary
        if not MPC.__client:
            MPC.__client = MPDClient()

            # attempt to connect
            try:
                MPC.__client.connect(host=settings.MPD_HOST, port=settings.MPD_PORT)
            except SocketError as e:
                MPC.__client = None
                raise MPCError("Could not connect : " + str(e))

            try:
                if settings.MPD_PASSWORD:
                    MPC.__client.password(settings.MPD_PASSWORD)
            except CommandError as e:
                MPC.__client.disconnect()
                MPC.__client = None
                raise MPCError("Could not auth : " + str(e))

    def __getattr__(self, name):
        return lambda *args : getattr(MPC.__client, name)(*args)