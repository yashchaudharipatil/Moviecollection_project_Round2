
from django.contrib import admin
from django.urls import path, include
from movie_collection import movie_views
from . import movie_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('collections.urls')),  # Include your app's URLs here
]
