from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework import serializers

from .models import User
from helpers.customFields import PasswordField

User = get_user_model()



class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        serializers = UserSerializerWithToken(self.user).data

        for k, v in serializers.items():
            data[k] = v

        return data
    
    

class UserSerializer(serializers.ModelSerializer):

    is_active = serializers.SerializerMethodField(read_only=True)
    is_staff = serializers.SerializerMethodField(read_only=True)
    
    
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "registration_complete",
            "is_active",
            "is_staff",
        ]
        
    def get_is_active(self, obj):
        return obj.is_active

    def get_is_staff(self, obj):
        return obj.is_staff


class UpdateUserSerializer(UserSerializer):
    
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'is_active',
                  'date_joined', 'fullname', 'is_staff']
        
         
        
class UserSerializerWithToken(UserSerializer):
    
    token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'registration_complete',
                  'is_active', 'date_joined', 'is_staff', 'token']

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)
    


class RegisterSerializer(UserSerializerWithToken):
    password = PasswordField(max_length=100, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name',
                   'password', 'registration_complete', 'token']
        
        

class LoginSerializer(RegisterSerializer):
    password = PasswordField(max_length=100, min_length=6, write_only=True)
    email = serializers.EmailField(max_length=200)

    class Meta:
        model = User
        fields = ['email', 'password', 'token']