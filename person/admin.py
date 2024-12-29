from django.contrib import admin
from django.utils.html import format_html
from .models import Profile, Marriage

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name',  'unique_id', 'gender', 'vitality', 'birth_date_display', 'death_date_display')
    search_fields = ('first_name', 'last_name', 'unique_id', 'birth_year', 'death_year')
    list_filter = ('gender', 'vitality')
    readonly_fields = ('display_full_siblings', 'display_half_siblings', 'familysearch_link')

    def display_full_siblings(self, obj):
        """
        Display only full siblings.
        """
        full_siblings = obj.get_full_siblings()
        if full_siblings.exists():
            return ", ".join([sibling.full_name for sibling in full_siblings])
        return "No full siblings"

    def display_half_siblings(self, obj):
        """
        Display only half siblings.
        """
        half_siblings = obj.get_half_siblings()
        if half_siblings.exists():
            return ", ".join([sibling.full_name for sibling in half_siblings])
        return "No half siblings"

    display_full_siblings.short_description = "Full Siblings"
    display_half_siblings.short_description = "Half Siblings"
    
    def familysearch_link(self, obj):
        """
        Returns a hyperlink to the FamilySearch profile.
        """
        if obj.familysearch_id:
            url = f"https://www.familysearch.org/tree/person/details/{obj.familysearch_id}"
            return format_html('<a href="{}" target="_blank">{}</a>', url, obj.familysearch_id)
        return "No FamilySearch ID"
    
@admin.register(Marriage)
class MarriageAdmin(admin.ModelAdmin):
    list_display = ('husband', 'wife', 'marriage_date_display')
    search_fields = ('husband__last_name', 'wife__last_name', 'marriage_date')
