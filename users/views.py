from django.shortcuts import render
from rest_framework import generics, permissions, status
from .models import *
from .serializers import LoginSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken # this gives us access to the refresh token



class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()

            response_data = {
                'message': 'User created succesfully',
                'status': status.HTTP_201_CREATED,
                'data': serializer.data
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        except Exception as e:
            response_data = {
                'message': 'User not created',
                'status': status.HTTP_400_BAD_REQUEST,
                'error': str(e)
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        try:

            serializer = LoginSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data['user']
            
            tokens = serializer.get_token(user)
            response_data = {
                'message': 'User logged in succesfully',
                'status': status.HTTP_200_OK,
                'data': tokens

            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            response_data = {
                'message': 'Invalid credentials',
                'status': status.HTTP_400_BAD_REQUEST,
                'error': str(e)
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
