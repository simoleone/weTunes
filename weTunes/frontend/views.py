from django.template import Context, loader
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from frontend.lib.mpc import MPC
from frontend.lib.queue import Queue
from frontend.models import Vote

def index(request):
    t = loader.get_template('index.html')

    song = MPC().currentsong()
    playlist = Queue().get_playlist()
    volume = MPC().status()['volume']

    c = Context({
        'song': song,
        'volume': volume,
        'playlist': playlist
    })
    return HttpResponse(t.render(c))

def search(request):
    return False

@login_required
def vote(request, filename):
    Vote.objects.get_or_create(user = request.user.username, filename = filename, played = False)
    Queue().save_queue()
    return index(request)

@login_required
def unvote(request):
    return False

@login_required
def setvolume(request, level):
    MPC().setvol(level)
    return index(request)

@login_required
def playpause(request):
    MPC().pause()
    return index(request)
