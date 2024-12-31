from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/person/', include('person.urls')),  # Include the person app's URLs
]
