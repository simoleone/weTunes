from django.template import Context, loader
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from frontend.lib.mpc import MPC
from frontend.lib.queue import Queue
from frontend.models import Vote
import json

def index(request):
    t = loader.get_template('index.html')

    song = MPC().currentsong()
    playlist = Queue().get_playlist()
    volume = MPC().status()['volume']

    c = Context({
        'song': song,
        'volume': volume,
        'playlist': playlist,
        'username': request.user.username,
    })
    return HttpResponse(t.render(c))

def search(request, field = None, value = None):
    if 'field' in request.REQUEST and 'value' in request.REQUEST:
        field = request.REQUEST['field']
        value = request.REQUEST['value']
    # field can be 'artist', 'title', or 'album', 'any'
    # this is garunteed by routing and so isn't checked
    t = loader.get_template('search.html')

    results = MPC().search(field, value)
    c = Context({
        'results': results,
    })
    return HttpResponse(t.render(c))

"Returns JSON data on the current state of mpd"
def ajax_mpd_status(request):
    # first set some sane defaults
    c = {}
    c['elapsed'] = 0
    c['cursong'] = {'time':1}

    # give them real values
    c.update(MPC().status())
    c['cursong'].update(MPC().currentsong())

    return HttpResponse(json.dumps(c))

@login_required
def vote(request, filename):
    Vote.objects.get_or_create(user = request.user.username, filename = filename, played = False)
    Queue().save_queue()
    MPC().play()
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
    if MPC().status()['state'] == 'stop':
        MPC().play()
    else:
        MPC().pause()
    return index(request)

@login_required
def updatedb(request):
    MPC().update()
    return index(request)
