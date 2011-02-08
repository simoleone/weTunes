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
    c = Context({
        'username': request.user.username,
    })
    return render_to_response("index.html", c, context_instance=RequestContext(request))

def search(request):
    c = Context()
    if 'searchterm' in request.POST:
        c = Context({
            'searchterm': request.POST['searchterm'],
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
    b = Block(length=0, author=request.user.username)
    b.save()
    i=0

    if len(songfiles) == 0:
        return HttpResponse("No Songs. Wtf mate?")

    for s in songfiles:
        dat = MPC().search('file', s)[0]
        Track(block=b, filename=s, track_number=i, artist=dat['artist'], album=dat['album'], title=dat['title']).save()
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
        trackdata = []
        voted = False

        for t in tracks:
            trackdata += [{'artist':t.artist, 'album':t.album, 'title': t.title}]

        if request.user.is_authenticated():
            try:
                v = Vote.objects.get(user = request.user.username, block = block)
                voted = v.id
            except Vote.DoesNotExist:
                pass


        returnlist += [{'author':block.author, 'id':block.id, 'voted':voted, 'tracks':trackdata}]
    return HttpResponse(json.dumps(returnlist))


@login_required
def ajax_vote(request, blockid):
    try:
        b = Block.objects.get(id=blockid)
    except Block.DoesNotExist:
        return HttpResponse("No such block")

    Vote.objects.get_or_create(user = request.user.username, block = b)
    Queue().save_queue()
    return HttpResponse("OK")

@login_required
def ajax_unvote(request, blockid):
    try:
        v = Vote.objects.get(block=blockid, user=request.user.username)
        v.delete()
    except Vote.DoesNotExist:
        return HttpResponse("No such vote")

    Queue().save_queue()
    return HttpResponse("OK")

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
