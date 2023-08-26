from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from .serializers import CollectionSerializer
from .models import Collection 
import requests
from rest_framework import generics

class UserRegistrationView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        if not username or not password:
            return Response({"error": "Both username and password are required."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if the username is already taken
        if User.objects.filter(username=username).exists():
            return Response({"error": "Username is already taken."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create a new user
        user = User.objects.create_user(username=username, password=password)
        
        # Generate and return a JWT token
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"access_token": token.key}, status=status.HTTP_201_CREATED)

# Movie Listing API (Integration with External API)
class MovieListView(generics.ListAPIView):
    def list(self, request):
        try:
            response = requests.get("https://demo.credy.in/api/v1/maya/movies/", auth=(MOVIE_API_USERNAME, MOVIE_API_PASSWORD))
            response.raise_for_status()  # Raise an exception for HTTP errors
            data = response.json()
            return Response(data.get("data", []))
        except requests.exceptions.RequestException as e:
            return Response({"error": "Error fetching movies from the external API."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Create collections
class CollectionCreateView(generics.CreateAPIView):
    serializer_class = CollectionSerializer  # Define the serializer for creating collections

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# Update collections
class CollectionUpdateView(generics.UpdateAPIView):
    serializer_class = CollectionSerializer  # Define the serializer for updating collections
    queryset = Collection.objects.all()

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

# Retrieve Collection
class CollectionDetailView(generics.RetrieveAPIView):
    serializer_class = CollectionSerializer  # Define the serializer for retrieving collections
    queryset = Collection.objects.all()

# Delete collections
class CollectionDeleteView(generics.DestroyAPIView):
    queryset = Collection.objects.all()
