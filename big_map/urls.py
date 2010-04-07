from django.conf.urls.defaults import *

urlpatterns = patterns('geodjango.big_map.views',
    (r'^big_map/(?P<chamber>upper|lower).kml$', 'big_map'),
)
