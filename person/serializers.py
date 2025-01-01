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
    
    class Meta:
        model = Profile
        fields = '__all__'
        
class MarriageSerializer(serializers.ModelSerializer):
    location = LocationSerializer(read_only=True)
    
    class Meta:
        model = Marriage
        fields = '__all__'