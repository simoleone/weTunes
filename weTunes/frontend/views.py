from django.template import Context, loader
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

def index(request):
    t = loader.get_template('index.html')
    c = Context({
        'song': song,
        'volume': volume,
        'playlist', playlist
    })
    return HttpResponse(t.render(c))

def search(request):
    return False

@login_required
def vote(request):
    return False

@login_required
def changevolume(request):
    return False

@login_required
def playpause(request):
    return False
