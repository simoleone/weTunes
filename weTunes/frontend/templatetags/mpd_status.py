from django import template
register = template.Library()

from frontend.lib.mpc import MPC

# just renders the currently playing song, volume, and so on
@register.inclusion_tag('templatetags/mpd_status.html')
def mpd_status():
    return None
