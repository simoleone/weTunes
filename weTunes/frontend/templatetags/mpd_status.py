from django import template
register = template.Library()

from frontend.lib.mpc import MPC

# just renders the currently playing song, volume, and so on
@register.inclusion_tag('templatetags/mpd_status.html')
def mpd_status():
    c = MPC().status()
    c['cursong'] = MPC().currentsong()
    return c
