from django.db import models

class Location(models.Model):
    LOCATION_TYPES = [
        ('COUNTRY', 'Country'),
        ('PROVINCE', 'Province/State'),
        ('DISTRICT', 'District/County'),
        ('REGION', 'Region/Zone'),
        ('MUNICIPALITY', 'Municipality'),
        ('CITY', 'City/Town/Village'),
        ('SUBURB', 'Suburb/Neighbourhood'),
        ('FARM', 'Farm/Plot'),
        ('STREET', 'Street/Lane/Avenue'),
        ('BUILDING', 'Building/Complex'),
        ('ROOM', 'Room/Office/Flat'), 
        ('CONSTITUENCY', 'Constituency/Ward'),
        ('WARD', 'Ward'),
        ('CANTON', 'Canton'),
        ('ISLAND', 'Island/Archipelago/Atoll'),
        ('AUTONOMOUS_REGION', 'Autonomous Region'),
        ('SAR', 'Special Administrative Region'),
    ]
    
    
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='location_parent')
    location_type = models.CharField(max_length=100, choices=LOCATION_TYPES)
    name = models.CharField(max_length=256)
    name_abbreviation = models.CharField(max_length=100, null=True, blank=True)
    name_year_start = models.IntegerField(null=True, blank=True)
    name_year_end = models.IntegerField(null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    
    class Meta:
        verbose_name = 'Location'
        verbose_name_plural = 'Locations'
    
    def has_coordinates(self):
        return self.latitude is not None and self.longitude is not None
    
    def has_no_parents(self):
        return self.parent is None and self.location_type != 'COUNTRY'
    
    def is_present_name(self):
        return self.name_year_end is None
    
    def __str__(self):
        if self.parent:
            return f"{self.name}, {self.parent.name}"
        return self.name