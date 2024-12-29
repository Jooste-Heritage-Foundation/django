import random
import string
from django.db import models
from location.models import Location

class Profile(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('U', 'Unknown'),
    ]
    
    VITALITY_CHOICES = [
        ('A', 'Alive'),
        ('D', 'Deceased'),
        ('U', 'Unknown'),
    ]
    
    unique_id = models.CharField(max_length=6, unique=True, editable=False, db_index=True)
    first_name = models.CharField(max_length=64, blank=True, null=True)
    last_name = models.CharField(max_length=64, blank=True, null=True)
    second_name = models.CharField(max_length=64, blank=True, null=True)
    known_as = models.CharField(max_length=64, blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    vitality = models.CharField(max_length=1, choices=VITALITY_CHOICES, blank=True, null=True)
    birth_year = models.IntegerField(blank=True, null=True)
    birth_month = models.IntegerField(blank=True, null=True)
    birth_day = models.IntegerField(blank=True, null=True)
    birth_circa = models.BooleanField(default=False, help_text="Is the birth date an approximate?")
    birth_date_range_start = models.DateField(blank=True, null=True, help_text="Start of birth date range (if known).")
    birth_date_range_end = models.DateField(blank=True, null=True, help_text="End of birth date range (if known).")
    birth_location = models.ForeignKey(Location, on_delete=models.SET_NULL, blank=True, null=True, related_name='birth_location')
    baptism_year = models.IntegerField(blank=True, null=True)
    baptism_month = models.IntegerField(blank=True, null=True)
    baptism_day = models.IntegerField(blank=True, null=True)
    baptism_circa = models.BooleanField(default=False, help_text="Is the baptism date an approximate?")
    baptism_date_range_start = models.DateField(blank=True, null=True, help_text="Start of baptism date range (if known).")
    baptism_date_range_end = models.DateField(blank=True, null=True, help_text="End of baptism date range (if known).")
    baptism_location = models.ForeignKey(Location, on_delete=models.SET_NULL, blank=True, null=True, related_name='baptism_location')
    death_year = models.IntegerField(blank=True, null=True)
    death_month = models.IntegerField(blank=True, null=True)
    death_day = models.IntegerField(blank=True, null=True)
    death_circa = models.BooleanField(default=False, help_text="Is the death date an approximate?")
    death_date_range_start = models.DateField(blank=True, null=True, help_text="Start of death date range (if known).")
    death_date_range_end = models.DateField(blank=True, null=True, help_text="End of death date range (if known).")
    death_location = models.ForeignKey(Location, on_delete=models.SET_NULL, blank=True, null=True, related_name='death_location')
    father = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True, related_name='children_by_father')
    mother = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True, related_name='children_by_mother')
    familysearch_id = models.CharField(max_length=64, blank=True, null=True)
    
    class Meta:
        verbose_name_plural = "Profiles"
        
    @property
    def full_name(self):
        """
        Returns the person's full name. Handles missing parts gracefully.
        """
        parts = [self.first_name, self.second_name, self.last_name]
        return " ".join(part for part in parts if part).strip() or "Unknown"
    
    def known_as_name(self):
        """
        Returns the person's known as name, if available, otherwise falls back.
        """
        return f"{self.known_as} {self.last_name}".strip()
    
    def get_siblings(self):
        """
        Returns a queryset of siblings, excluding the current person.
        """
        siblings_from_father = Profile.objects.filter(father=self.father).exclude(id=self.id) if self.father else Profile.objects.none()
        siblings_from_mother = Profile.objects.filter(mother=self.mother).exclude(id=self.id) if self.mother else Profile.objects.none()
        
        # Combine siblings from both parents
        siblings = siblings_from_father | siblings_from_mother
        
        # Use `.distinct()` to avoid duplicates when both parents are shared
        return siblings.distinct()
    
    def get_full_siblings(self):
        """
        Returns a queryset of full siblings (sharing both the same father and mother).
        """
        if self.father and self.mother:
            return Profile.objects.filter(father=self.father, mother=self.mother).exclude(id=self.id)
        return Profile.objects.none()
    
    def get_half_siblings(self):
        """
        Returns a queryset of half-siblings (sharing only one parent).
        """
        siblings_from_father = Profile.objects.filter(father=self.father).exclude(id=self.id) if self.father else Profile.objects.none()
        siblings_from_mother = Profile.objects.filter(mother=self.mother).exclude(id=self.id) if self.mother else Profile.objects.none()
        
        # Subtract full siblings to get half-siblings only
        return (siblings_from_father | siblings_from_mother).distinct().difference(self.get_full_siblings())
        
        
    def save(self, *args, **kwargs):
        if not self.unique_id:
            self.unique_id = self.generate_unique_id()
        super().save(*args, **kwargs)
        
    @staticmethod
    def generate_unique_id():
        """
        Generate a random 6-character alphanumeric string.
        Ensures the ID is unique by checking existing records.
        """
        from person.models import Profile  # Avoid circular import issues
        while True:
            random_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            if not Profile.objects.filter(unique_id=random_id).exists():
                return random_id
    
    def __str__(self):
        """
        Returns a string representation of the Profile including key details for disambiguation.
        """
        birth_year = self.birth_year or " "
        death_year = self.death_year or " "
        if self.vitality == 'A':
            return f"{self.full_name} (*. {birth_year})"
        elif self.vitality == 'D':
            return f"{self.full_name} (*. {birth_year} - †. {death_year})"
    
    def get_flexible_date(self, year, month, day, circa):
        """
        Returns a formatted date string based on the available fields.
        """
        if year and not  month and not day:
            date_str = f"circa {year}" if circa else f"{year}"
        elif year and month and not day:
            date_str = f"circa {year}-{month:02}" if circa else f"{year}-{month:02}"
        elif year and month and day:
            date_str = f"circa {year}-{month:02}-{day:02}" if circa else f"{year}-{month:02}-{day:02}"
        else:
            date_str = "Unknown"
        return date_str
    
    def birth_date_display(self):
        return self.get_flexible_date(self.birth_year, self.birth_month, self.birth_day, self.birth_circa)
    
    def baptism_date_display(self):
        return self.get_flexible_date(self.baptism_year, self.baptism_month, self.baptism_day, self.baptism_circa)
    
    def death_date_display(self):
        return self.get_flexible_date(self.death_year, self.death_month, self.death_day, self.death_circa)
    
class Marriage(models.Model):
    husband = models.ForeignKey(Profile, related_name='husbands', on_delete=models.SET_NULL, blank=True, null=True)
    wife = models.ForeignKey(Profile, related_name='wives', on_delete=models.SET_NULL, null=True)
    marriage_year = models.IntegerField(blank=True, null=True)
    marriage_month = models.IntegerField(blank=True, null=True)
    marriage_day = models.IntegerField(blank=True, null=True)
    marriage_circa = models.BooleanField(default=False, help_text="Is the marriage date an approximate?")
    marriage_date_range_start = models.DateField(blank=True, null=True, help_text="Start of marriage date range (if known).")
    marriage_date_range_end = models.DateField(blank=True, null=True, help_text="End of marriage date range (if known).")
    marriage_status = models.CharField(max_length=64, choices=[
        ('M', 'Married'),
        ('D', 'Divorced'),
        ('S', 'Separated'),
        ('U', 'Unknown'),
    ], default='M')
    marriage_location = models.ForeignKey(Location, on_delete=models.SET_NULL, blank=True, null=True, related_name='location_of_marriage')
    
    divorce_year = models.IntegerField(blank=True, null=True)
    divorce_month = models.IntegerField(blank=True, null=True)
    divorce_day = models.IntegerField(blank=True, null=True)
    divorce_circa = models.BooleanField(default=False, help_text="Is the divorce date an approximate?")
    divorce_date_range_start = models.DateField(blank=True, null=True, help_text="Start of divorce date range (if known).")
    divorce_date_range_end = models.DateField(blank=True, null=True, help_text="End of divorce date range (if known).")
    
    class Meta:
        verbose_name_plural = "Marriages"
        
    def __str__(self):
        return f"{self.husband} & {self.wife} - {self.marriage_year}"
    
    def get_flexible_date(self, year, month, day, circa):
        """
        Returns a formatted date string based on the available fields.
        """
        if year and not  month and not day:
            date_str = f"circa {year}" if circa else f"{year}"
        elif year and month and not day:
            date_str = f"circa {year}-{month:02}" if circa else f"{year}-{month:02}"
        elif year and month and day:
            date_str = f"circa {year}-{month:02}-{day:02}" if circa else f"{year}-{month:02}-{day:02}"
        else:
            date_str = "Unknown"
        return date_str
    
    def marriage_date_display(self):
        return self.get_flexible_date(self.marriage_year, self.marriage_month, self.marriage_day, self.marriage_circa)
    
    def divorce_date_display(self):
        return self.get_flexible_date(self.divorce_year, self.divorce_month, self.divorce_day, self.divorce_circa)