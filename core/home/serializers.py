from rest_framework import serializers
from home.models import Person, Color
from django.contrib.auth.models import User 

class RegisterSerializers(serializers.Serializer):
    username=serializers.CharField()
    email=serializers.EmailField()
    password=serializers.CharField()

    def validate(self, data):
        username = data.get('username')  # Corrected the variable name
        email = data.get('email')  # Corrected the variable name

        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError('Username is taken')

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Email is taken')

        return data
    def create(self, validated_data):
        # Create a new user instance
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email']
        )
        # Set the password for the user
        user.set_password(validated_data['password'])
        user.save()
        return user

class LoginSerializers(serializers.Serializer):
    username=serializers.CharField()
    password = serializers.CharField()

class ColorSerializers(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ['Colour_name']

class PeopleSerializers(serializers.ModelSerializer):
    color = ColorSerializers()
    color_info = serializers.SerializerMethodField()

    class Meta:
        model = Person
        fields = ['name', 'age', 'color', 'color_info']
        
    def get_color_info(self, obj):
        if obj.color:
            colour_obj = Color.objects.get(id=obj.color.id)
            return {'color_name': colour_obj.Colour_name, 'hex_code': '#000'}
        return None
    def validate(self, data):
        if data['age'] < 18:
            raise serializers.ValidationError('NOT 18+')
        return data
