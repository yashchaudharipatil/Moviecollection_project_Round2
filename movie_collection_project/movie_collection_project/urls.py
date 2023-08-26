
from django.urls import path
#from . import movie_views
from movie_collection import movie_views

urlpatterns = [
    path('collection/create/', movie_views.CollectionCreateView.as_view(), name='collection-create'),
    path('collection/<int:pk>/update/', movie_views.CollectionUpdateView.as_view(), name='collection-update'),
    path('collection/<int:pk>/', movie_views.CollectionDetailView.as_view(), name='collection-detail'),
    path('collection/<int:pk>/delete/', movie_views.CollectionDeleteView.as_view(), name='collection-delete'),
]
