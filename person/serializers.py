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
    spouse_name = serializers.SerializerMethodField()
    spouse_unique_id = serializers.SerializerMethodField()
    marriage_location = serializers.StringRelatedField()
    children = ProfileSerializer(many=True, read_only=True)
    
    is_active = serializers.SerializerMethodField()
    
    class Meta:
        model = Marriage
        fields = '__all__'
        
    def get_spouse_name(self, obj):
        profile = self.context.get('profile')  # Get the profile from the context

        # Return the name of the spouse who is not the profile person
        if profile:
            if obj.spouse1 == profile:
                return f"{obj.spouse2.first_name} {obj.spouse2.last_name}"
            elif obj.spouse2 == profile:
                return f"{obj.spouse1.first_name} {obj.spouse1.last_name}"
        return None  # In case no profile is provided or no match is found
        
    def get_is_active(self, obj):
        # Call the is_active method from the Marriage model
        return obj.is_active()
    
    def get_spouse_unique_id(self, obj):
        profile = self.context.get('profile')
        
        # Return the unique_id of the spouse who is not the profile person
        if profile:
            if obj.spouse1 == profile:
                return obj.spouse2.unique_id
            elif obj.spouse2 == profile:
                return obj.spouse1.unique_id
        return None