from rest_framework.decorators import api_view
from rest_framework.response import Response
from home.models import Person
#from home.serializers import *
from home.serializers import LoginSerializers
from rest_framework.views import APIView
from rest_framework import viewsets
from home.serializers import PeopleSerializers # Import the PeopleSerializers class
from home.serializers import RegisterSerializers
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework import serializers
from home.models import Person
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication,BasicAuthentication 
from django.db.models import Q
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from  rest_framework.decorators import action
from django.core.paginator import Paginator

from rest_framework.response import Response
from rest_framework import viewsets


class LoginAPI(APIView):
    def post(Self,request):
        data=request.data 
        serializer=LoginSerializers(data=data)
        if not serializer.is_valid():
            return Response({
                'status': False,
                'message': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        User=authenticate(username = serializer.data['username'],password=serializer.data['password'])
        token,created=Token.objects.get_or_create(user=User)

        return Response({'status' : True,'message':'user login','token':str(token)},status=status.HTTP_201_CREATED)


class ResisterAPI(APIView):
    def post(self,request):
        data=request.data 
        serializer=RegisterSerializers(data=data)

        if not serializer.is_valid():
            return Response({
                'status': False,
                'message': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({'status' : True,'message':'user created'},status=status.HTTP_201_CREATED)

class PeopleSerializers(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'



@api_view(['GET','POST','PUT'])
def index(request):

    courses = {
        'course_name': 'Python',
        'learn': ['flask', 'Django', 'Tornado', 'FastApi'],
        'course_provider': 'Scaler'
    }

    

    if request.method=='GET':
        print('GET method called')
        return Response(courses)

    elif request.method=='POST':
        data=request.data 
        print('***')
        print(data)
        print('***')
        print('POST method is called')
        return Response()
    elif request.method=='PUT':
            print('PUT method is called')
            return Response()
    else:
         data=request.data
         print(data)
         json_responce={
              'name':'Scaler',
              'Course':['C++','Python'],
              'method':'Post'
         }
    return Response(json_responce)

@api_view(['POST'])
def login(request):
    data = request.data 
    serializer = LoginSerializers(data=data)

    if serializer.is_valid():
        validated_data = serializer.validated_data
        # Process your validated data here
        return Response({'message': 'SUCCESS'})

    return Response(serializer.errors)

class PersonApi(APIView):
   # permission_classes=[IsAuthenticated]
   # authentication_classes=[TokenAuthentication]

    def get(self, request):
        print(request.user)
        # Filter Person objects where the color field is not null
        objs = Person.objects.filter(~Q(color=None))

        page = request.GET.get('page', 1)
        page_size = 3
        paginator = Paginator(objs, page_size)  # Define Paginator here

        try:
            page_data = paginator.page(page)
        except EmptyPage:
            # Handle the case when the requested page is empty
            return Response({'message': 'Page is empty'}, status=status.HTTP_404_NOT_FOUND)
        except PageNotAnInteger:
            # Handle the case when the page parameter is not an integer
            return Response({'message': 'Invalid page number'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = PeopleSerializers(page_data, many=True)
        return Response(serializer.data)


    def post(self , request):
        return Response({'message':'post request '})

    def put(self , request):
        return Response({'message':'put request '})

    def patch(self , request):
        return Response({'message':'patch request '})
    def delete(self , request):
        return Response({'message':'delete request '})
    

@api_view(['GET', 'POST','PUT','PATCH','DELETE'])

def people(request):
    if request.method == 'GET':
        objs = Person.objects.all()
        serializer = PeopleSerializers(objs, many=True)
        return Response(serializer.data)
    elif request.method=="POST":
        data = request.data
        serializer = PeopleSerializers(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    elif request.method=='PUT':
        data = request.data
        serializer = PeopleSerializers(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)         
    elif request.method=='PATCH':
        data = request.data
       # obj=Person.objects.get(id=data['id'])
        serializer = PeopleSerializers(data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)         
    elif request.method == 'DELETE':
        data = request.data
        objs = Person.objects.filter(name=data['name'])
        if objs.exists():
            objs.delete()
            return Response({'message': 'person deleted'})
        else:
            return Response({'message': 'person not found'})





class PeopleViewset(viewsets.ModelViewSet):
    serializer_class = PeopleSerializers  # Use the correct serializer class name
    queryset = Person.objects.all()  # Correct the queryset attribute

    def list(self ,request):
        search=request.GET.get('search')
        queryset=self.queryset
        if search:
            queryset=queryset.filter(name__startswith=search)
        serializer=PeopleSerializers(queryset,many=True)

        return Response({'status':200,'data':serializer.data})


    @action(detail=True, methods=['POST'])
    def send_email_to_person(self, request,pk):
        obj=Person.objects.get(pk=pk)
        serializer=PeopleSerializers(obj)
        return Response({
            'status': True,
            'message': 'email sent successfully',
            'data':serializer.data 
        })


