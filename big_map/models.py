from django.contrib.gis.db import models
from django.db.models.signals import pre_save

class District(models.Model):
    state_abbrev = models.CharField(max_length=2)
    chamber = models.CharField(max_length=5)
    sld = models.CharField(max_length=3)
    name = models.CharField(max_length=200)
    lsad = models.CharField(max_length=2)
    geo_id = models.CharField(max_length=12)
    lsad_trans = models.CharField(max_length=50)
    geom = models.MultiPolygonField(srid=4326)
    objects = models.GeoManager()

    party = models.CharField(max_length=200, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __unicode__(self):
        return "%s %s %s" % (self.state_abbrev.upper(), self.chamber,
                             self.name)


    @property
    def current_party(self):
        if self.legislator_set.count() == 0:
            return 'Empty'

        dems = self.legislator_set.filter(party__startswith='Democrat').count()
        repubs = self.legislator_set.filter(party__startswith='Republican').count()
        indps = self.legislator_set.filter(party__startswith='Independent').count()
        other = self.legislator_set.count() - (dems + repubs + indps)

        if dems > 0 and (repubs + indps + other) == 0:
            return 'Democrat'

        if repubs > 0 and (dems + indps + other) == 0:
            return 'Republican'

        if indps > 0 and (dems + repubs + other) == 0:
            return 'Independent'

        if dems > 0 and repubs > 0 and (other + indps) == 0:
            return 'Purple'

        return 'Other'


def process_district(sender, **kwargs):
    instance = kwargs['instance']
    if instance.pk is not None:
        return
    instance.state_abbrev = state_nums[instance.state_abbrev]
    instance.name = instance.name.lstrip('0')
    #if instance.lsad == 'LU' or instance.lsad == 'L7':
    instance.chamber = 'upper'
    #elif instance.lsad == 'LL' or instance.lsad == 'L3':
    #    instance.chamber = 'lower'
    instance.name = instance.name.replace('Distict', 'District')
pre_save.connect(process_district, sender=District)

class Legislator(models.Model):
    district = models.ForeignKey(District)
    full_name = models.CharField(max_length=200)
    party = models.CharField(max_length=200)


state_nums = {
    '01': 'al',
    '02': 'ak',
    '04': 'az',
    '05': 'ar',
    '06': 'ca',
    '08': 'co',
    '09': 'ct',
    '10': 'de',
    '11': 'dc', # unicameral city council
    '12': 'fl',
    '13': 'ga',
    '15': 'hi',
    '16': 'id',
    '17': 'il',
    '18': 'in',
    '19': 'ia',
    '20': 'ks',
    '21': 'ky',
    '22': 'la',
    '23': 'me',
    '24': 'md',
    '25': 'ma',
    '26': 'mi',
    '27': 'mn',
    '28': 'ms',
    '29': 'mo',
    '30': 'mt',
    '31': 'ne', # unicameral
    '32': 'nv',
    '33': 'nh',
    '34': 'nj',
    '35': 'nm',
    '36': 'ny',
    '37': 'nc',
    '38': 'nd',
    '39': 'oh',
    '40': 'ok',
    '41': 'or',
    '42': 'pa',
    '44': 'ri',
    '45': 'sc',
    '46': 'sd',
    '47': 'tn',
    '48': 'tx',
    '49': 'ut',
    '50': 'vt',
    '51': 'va',
    '53': 'wa',
    '54': 'wv',
    '55': 'wi',
    '56': 'wy',
    '72': 'pr'
}
    
# Auto-generated `LayerMapping` dictionary for District model
upper_district_mapping = {
    'state_abbrev' : 'STATE',
    'sld' : 'SLDU',
    'name' : 'NAME',
    'lsad' : 'LSAD',
    'geo_id' : 'GEO_ID',
    'lsad_trans' : 'LSAD_TRANS',
    'geom' : 'MULTIPOLYGON',
}

lower_district_mapping = {
    'state_abbrev' : 'STATE',
    'sld' : 'SLDL',
    'name' : 'NAME',
    'lsad' : 'LSAD',
    'geo_id' : 'GEO_ID',
    'lsad_trans' : 'LSAD_TRANS',
    'geom' : 'MULTIPOLYGON',
}
