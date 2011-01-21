from django.conf.urls.defaults import *


urlpatterns = patterns('',
    (r'^vote/(?P<filename>.*)$', 'frontend.views.vote'),
    (r'^unvote/(?P<filename>.*)$', 'frontend.views.unvote'),
    (r'^search/(?P<terms>.*)$', 'frontend.views.search'),
    (r'^setvolume/(?P<level>\d{1,3})$', 'frontend.views.setvolume'),
    (r'', 'frontend.views.index'),
    # Example:
    # (r'^weTunes/', include('weTunes.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)
