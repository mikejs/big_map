from django.core.management.base import BaseCommand
from django.conf import settings
from django.contrib.gis.utils.layermapping import LayerMapping
import os
import urllib2
import zipfile
from cStringIO import StringIO
from big_map.big_map import models

class Command(BaseCommand):
    def handle(self, *args, **options):
        for num, abbrev in models.state_nums.items():
            print "Importing %s" % abbrev.upper()

            su_path = os.path.abspath(os.path.join(
                    os.path.dirname(models.__file__),
                    'data/su%s_d11.shp' % num))

            try:
                mapping = LayerMapping(models.District, su_path,
                                       models.upper_district_mapping,
                                       source_srs=4296,
                                       transform=True)
            except:
                print "Downloading su%s_d11_shp.zip" % num
                data = urllib2.urlopen("http://www.census.gov/geo/cob/bdy/su/su06shp/su%s_d11_shp.zip" % num).read()
                data = StringIO(data)
                zip = zipfile.ZipFile(data)
                zip.extractall(os.path.abspath(os.path.join(
                            os.path.dirname(models.__file__), 'data/')))
                mapping = LayerMapping(models.District, su_path,
                                       models.upper_district_mapping,
                                       source_srs=4296,
                                       transform=True)

            mapping.save(strict=True)

            if abbrev.lower() == 'dc' or abbrev.lower() == 'ne':
                continue
            
     #       sl_path = os.path.abspath(os.path.join(
     #               os.path.dirname(models.__file__),
     #               'data/sl%s_d11.shp' % num))

     #       try:
     #           mapping = LayerMapping(models.District, sl_path,
     #                                  models.lower_district_mapping,
     #                                  transform=False)
#             except:
#                 print "Downloading sl%s_d11_shp.zip" % num
#                 data = urllib2.urlopen("http://www.census.gov/geo/cob/bdy/sl/sl06shp/sl%s_d11_shp.zip" % num).read()
#                 data = StringIO(data)
#                 zip = zipfile.ZipFile(data)
#                 zip.extractall(os.path.abspath(os.path.join(
#                             os.path.dirname(models.__file__), 'data/')))
#                 mapping = LayerMapping(models.District, sl_path,
#                                        models.lower_district_mapping,
#                                        transform=False)

#             mapping.save(strict=True)
