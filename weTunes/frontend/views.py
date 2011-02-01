from django.shortcuts import render_to_response
from django.template import Context, loader, RequestContext
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from frontend.lib.mpc import MPC
from frontend.lib.queue import Queue
from frontend.models import Vote, Block, Track
import json
from itertools import groupby

def index(request):
    song = MPC().currentsong()
    playlist = MPC().playlistinfo()

    c = Context({
        'song': song,
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
@csrf_exempt
def ajax_createblock(request):
    songfiles = json.loads(request.raw_post_data)
    b = Block(length=0)
    b.save()
    i=0
    for s in songfiles:
        Track(block=b, filename=s, track_number=i).save()
        i=i+1
    b.update_length()
    Vote(block=b, user=request.user.username).save()
    Queue().save_queue()
    return HttpResponse("OK")

""" Returns the current playlist in the format:
    [{author:name, id:id, tracks:[tracks]}, ...]
"""
def ajax_playlist(request):
    returnlist = []
    for block, tracks in groupby(Queue().save_queue(),lambda x : x.block):
        returnlist += [{'author':block.author, 'id':block.id, 'tracks':tracks}]
    return HttpResponse(json.dumps(returnlist))


@login_required
def vote(request, blockid):
    try:
        b = Block.objects.get(id=blockid)
    except Block.DoesNotExist:
        return HttpResponse("No such block")

    Vote.objects.get_or_create(user = request.user.username, block = b)
    Queue().save_queue()
    return index(request)

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
