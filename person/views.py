from rest_framework import generics
from .models import Profile, Marriage
from .serializers import ProfileSerializer, MarriageSerializer
from rest_framework.exceptions import NotFound

class ProfileListView(generics.ListAPIView):
    """
    Read-only view to list all profiles.
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    
class ProfileDetailView(generics.RetrieveAPIView):
    """
    Read-only view to retrieve a single profile by ID.
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    
    def get_object(self):
        """
        Override get_object to retrieve the profile by unique_id.
        """
        unique_id = self.kwargs.get('unique_id')  # Get the unique_id from the URL
        try:
            return Profile.objects.get(unique_id=unique_id)  # Filter by unique_id instead of pk
        except Profile.DoesNotExist:
            raise NotFound("Profile with this unique_id does not exist.")
    
class MarriageListView(generics.ListAPIView):
    """
    Read-only view to list all marriages.
    """
    queryset = Marriage.objects.all()
    serializer_class = MarriageSerializer
    
class MarriageDetailView(generics.RetrieveAPIView):
    """
    Read-only view to retrieve a single marriage by ID.
    """
    queryset = Marriage.objects.all()
    serializer_class = MarriageSerializer
