from django.contrib.gis import admin
from big_map.big_map.models import District, Legislator

admin.site.register(District, admin.GeoModelAdmin)
admin.site.register(Legislator)
