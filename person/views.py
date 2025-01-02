from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .utils import get_birthdays_in_next_three_months
from .models import Profile, Marriage
from django.http import JsonResponse
from .serializers import ProfileSerializer, MarriageSerializer
from rest_framework.exceptions import NotFound
from django.db.models import Q
from django.shortcuts import get_object_or_404

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
        
    def retrieve(self, request, *args, **kwargs):
        """
        Override retrieve to add marriage information along with profile data.
        """
        profile = self.get_object()
        
        # Fetch marriages associated with this profile
        marriages = Marriage.objects.filter(
            Q(spouse1=profile) | Q(spouse2=profile)
        ).select_related('spouse1', 'spouse2')

        # Serialize the profile and marriages, using context to exclude the profile person
        profile_data = ProfileSerializer(profile).data
        marriages_data = MarriageSerializer(marriages, many=True, context={'profile': profile}).data
        
        # Return profile and marriages in the response
        return Response({
            'profile': profile_data,
            'marriages': marriages_data,
        })
        
    def get_serializer_context(self):
        """
        Add the profile to the context so it can be accessed in the serializer.
        """
        context = super().get_serializer_context()
        profile = self.get_object()  # Get the current profile
        context['profile'] = profile  # Add the profile to the context
        return context

    
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
    
class UpcomingBirthdaysAPIView(APIView):
    name = "Birthdays"
    description = "Get upcoming birthdays in the next 3 months."
    def get(self, request):
        profiles = get_birthdays_in_next_three_months()
        serializer = ProfileSerializer(profiles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    