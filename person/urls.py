from django.urls import path
from .views import ProfileListView, ProfileDetailView

urlpatterns = [
    path('profiles/', ProfileListView.as_view(), name='profile-list'),
    path('profiles/<str:unique_id>/', ProfileDetailView.as_view(), name='profile-detail'),  # Use unique_id instead of pk
]
