from django.conf.urls.defaults import *


urlpatterns = patterns('',
    # actual frontend stuff
    (r'^vote/(?P<filename>.*)$', 'frontend.views.vote'),
    (r'^unvote/(?P<filename>.*)$', 'frontend.views.unvote'),
    (r'^search/(?P<terms>.*)$', 'frontend.views.search'),
    (r'^setvolume/(?P<level>\d{1,3})$', 'frontend.views.changevolume'),

    # login stuff
    (r'^account/login$', 'django.contrib.auth.views.login', {'template_name': 'account/login.html'}),
    (r'^account/logout$', 'django.contrib.auth.views.logout', {'template_name': 'account/logout.html'}),

    # default
    (r'', 'frontend.views.index'),

    # Example:
    # (r'^weTunes/', include('weTunes.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)
