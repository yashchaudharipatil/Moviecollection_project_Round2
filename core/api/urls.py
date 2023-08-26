from django.urls import path,include
from home import views
from home.views import *
from django.urls import path, include
from home.views import (
    index, login, PersonApi, PeopleViewset, ResisterAPI
)

from home.views import index,login,PersonApi,PeopleViewset,ResisterAPI
from rest_framework.routers import DefaultRouter
from home.views import index, login, PersonApi, PeopleViewset, ResisterAPI




router = DefaultRouter()
#router.register(r'peopleview', PeopleViewset, basename='people')
#urlpatterns = router.urls

router.register(r'peopleview', PeopleViewset, basename='people')


urlpatterns = [
    # ... other paths ...
    path('login/', login, name='login'),
    path('index/', index, name='index'),
    path('register/', ResisterAPI.as_view(), name='register'),
    path('people/', people, name='people'),
    path('persons/', PersonApi.as_view(), name='persons'),
]

# Include the router URLs
urlpatterns += router.urls
