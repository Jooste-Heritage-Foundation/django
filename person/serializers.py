from rest_framework import serializers
from .models import Profile, Marriage

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'
        
class MarriageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marriage
        fields = '__all__'