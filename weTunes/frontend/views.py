from django.shortcuts import render_to_response
from django.template import Context, loader, RequestContext
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from frontend.lib.mpc import MPC
from frontend.lib.queue import Queue
from frontend.models import Vote
import json

def index(request):
    song = MPC().currentsong()
    playlist = Queue().get_playlist()
    volume = MPC().status()['volume']

    c = Context({
        'song': song,
        'volume': volume,
        'playlist': playlist,
        'username': request.user.username,
    })
    return render_to_response("index.html", c, context_instance=RequestContext(request))

def search(request):
    c = Context()
    if 'field' in request.REQUEST and 'value' in request.REQUEST:
        c = Context({
            'field': request.REQUEST['field'],
            'value': request.REQUEST['value'],
        })
    return render_to_response("search.html", c, context_instance=RequestContext(request))

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

"Returns JSON data for a search"
def ajax_search(request):
    if not request.POST['field'] in ['artist','title','album','any']:
        raise HttpResponseBadRequest()

    c = MPC().search(request.POST['field'], request.POST['value'])
    return HttpResponse(json.dumps(c))

"Creates a block from provided file list"
@login_required
def ajax_createblock(request):
    block = json.loads(request.POST.keys()[0])
    return HttpResponse("OK")

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

@login_required
def next(request):
    MPC().next()
    return index(request)
