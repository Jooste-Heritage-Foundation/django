from django.contrib import admin
from .models import Location

class LocationAdmin(admin.ModelAdmin):
    # Fields to display in the list view
    list_display = ('name', 'name_year_start', 'name_year_end', 'location_type', 'parent', 'is_present_name', 'has_coordinates')
    
    # Filter options in the right sidebar
    list_filter = ('location_type', 'parent', 'has_coordinates')
    
    # Fields that should be searchable
    search_fields = ('name', 'location_type', 'latitude', 'longitude')
    
    # Fields for which we can create filters on the list view
    list_filter = ('location_type', 'parent')
    
    def is_present_name(self, obj):
        return obj.name_year_end is None
    is_present_name.boolean = True
    is_present_name.short_description = 'Present Name'
    
    # Add a helper method for checking if the location has coordinates
    def has_coordinates(self, obj):
        return obj.latitude is not None and obj.longitude is not None
    has_coordinates.boolean = True
    has_coordinates.short_description = 'Has Coordinates'
    
    # Add a helper method to check if the location has no parents (other than countries)
    def has_no_parents(self, obj):
        return obj.parent is None and obj.location_type != 'COUNTRY'
    has_no_parents.boolean = True
    has_no_parents.short_description = 'No Parent (Country only)'

# Register the Location model and apply the custom admin class
admin.site.register(Location, LocationAdmin)
