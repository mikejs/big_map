from big_map.big_map.models import District
from django.contrib.gis.shortcuts import render_to_kml

def big_map(request, chamber):
    districts = District.objects.filter(chamber=chamber).kml()

    return render_to_kml('big_map.kml', {'places': districts})
