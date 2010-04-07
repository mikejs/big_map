from django.core.management.base import BaseCommand
from django.conf import settings
from django.contrib.gis.utils import LayerMapping
import os
from big_map.big_map.models import state_nums, Legislator, District
from votesmart import votesmart

votesmart.apikey = settings.VOTESMART_API_KEY

class Command(BaseCommand):
    def handle(self, *args, **options):
        for num, abbrev in state_nums.items():
            if Legislator.objects.filter(
                district__state_abbrev=abbrev.lower()).count() > 0:
                continue

            print "Importing %s" % abbrev.upper()

            # 9=S, 7=A, 8=H

            if abbrev == 'dc' or abbrev == 'pr':
                continue
            
            for official in votesmart.officials.getByOfficeState(9,
                                                                 abbrev.upper()):

                try:
                    district = District.objects.get(
                        state_abbrev=abbrev.lower(),
                        name=official.officeDistrictId,
                        chamber='upper')
                except District.DoesNotExist:
                    try:
                        name = official.officeDistrictName

                        if name.startswith('Clark'):
                            name = name.replace('Clark',
                                                'Clark County Senatorial District')
                        elif name.startswith('Washoe'):
                            name = name.replace('Washoe',
                                                'Washoe County Senatorial District')
                        elif name == 'Northern Nevada':
                            name = 'Rural Nevada'
                        elif abbrev == 'ma':
                            name = name.replace(' and ', ' & ')
                            if ',' in name:
                                name = name + ' District'
                        name = name.strip()
                            
                        district = District.objects.get(
                            state_abbrev=abbrev.lower(),
                            name=name,
                            chamber='upper')
                    except District.DoesNotExist:
                        print "Not found: %s" % name
                        continue

                Legislator.objects.create(full_name=unicode(official),
                                          district=district,
                                          party=official.officeParties)
