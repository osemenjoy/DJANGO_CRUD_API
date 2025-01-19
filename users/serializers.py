from .models import *
from .views import *
from rest_framework import serializers
from django.db import transaction
import re
from django.contrib.auth import authenticate

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'role', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password is too short")
        if not re.search(r'\d', value):
            raise serializers.ValidationError("Password must contain at least one digit")
        if not re.search(r'[A-Za-z]', value):
            raise serializers.ValidationError("Password must contain at least one letter")
        if not re.search(r'[!@#$%^&*]', value):
            raise serializers.ValidationError("Password must contain at least one special character")
        return value

    def create(self, validated_data):
        with transaction.atomic():
            user = CustomUser.objects.create_user(
                username = validated_data["username"],
                email = validated_data["email"],
                password = validated_data["password"],
                role = validated_data["role"]
            )
            return user
        
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        
        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                data['user'] = user
            else:
                raise serializers.ValidationError("Invalid Credentials")
        else:
            raise serializers.ValidationError("Must include 'username' and 'password'")
        
        return data

    def get_token(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }