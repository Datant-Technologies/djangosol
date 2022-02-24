from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import  RefreshToken

from rest_framework import status



from account.models import User
from .serializers import UserSerializer, LoginSerializer, MyTokenObtainPairSerializer, RegisterSerializer, UpdateUserSerializer


class RegisterUserView(generics.CreateAPIView):
    """
    Create a new user in the system
    """
    serializer_class = UserSerializer
    http_method_names= ['post']
    
    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save()
            user_data = serializer.data
            user = User.objects.get(email = user_data['email'])
            token = RefreshToken.for_user(user).access_token
            user_context = {
                'user_data': user,
            }
            return Response({'message': 'Registered successfully', 'context': user_context},status=status.HTTP_201_CREATED )
        
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 


class LoginUserAPIView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer  