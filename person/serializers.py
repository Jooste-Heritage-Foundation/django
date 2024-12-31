from rest_framework import serializers
from .models import Profile, Marriage
from location.models import Location
from datetime import date

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'

class ProfileSerializer(serializers.ModelSerializer):
    location = LocationSerializer(read_only=True)
    current_age = serializers.SerializerMethodField()
    
    class Meta:
        model = Profile
        fields = '__all__'

    def get_current_age(self, obj):
        today = date.today()
        if obj.birth_year:
            # Calculate the age and adjust if the birthday hasn't occurred yet this year
            age = today.year - obj.birth_year
            if (obj.birth_month, obj.birth_day) > (today.month, today.day):
                age -= 1
            return age
        return None
        
class MarriageSerializer(serializers.ModelSerializer):
    location = LocationSerializer(read_only=True)
    
    class Meta:
        model = Marriage
        fields = '__all__'