from rest_framework import serializers
from .models import Profile, Marriage
from location.models import Location

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'

class ProfileSerializer(serializers.ModelSerializer):
    father_unique_id = serializers.CharField(source="father.unique_id", read_only=True)
    mother_unique_id = serializers.CharField(source="mother.unique_id", read_only=True)
    full_siblings_unique_id = serializers.SerializerMethodField()
    half_siblings_unique_id = serializers.SerializerMethodField()
    location = LocationSerializer(read_only=True)
    
    class Meta:
        model = Profile
        fields = '__all__'
        
    def get_full_siblings_unique_id(self, obj):
        return list(obj.get_full_siblings().values_list("unique_id", flat=True))

    def get_half_siblings_unique_id(self, obj):
        return list(obj.get_half_siblings().values_list("unique_id", flat=True))
        
class MarriageSerializer(serializers.ModelSerializer):
    location = LocationSerializer(read_only=True)
    
    class Meta:
        model = Marriage
        fields = '__all__'