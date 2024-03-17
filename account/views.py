from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

from .renderers import UserRenderer
from .serializers import *

# Create your views here.
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh':str(refresh),
        'access':str(refresh.access_token)
    }

class UserRegistrationView(APIView):
    renderer_classes = [UserRenderer]
    def post(self,request,format=None):
        serializer=UserRegistrationSerializer(data=request.data)
        # print(request.data)
        if serializer.is_valid(raise_exception=True):
            print(serializer.validated_data)
            user=serializer.save()
            token = get_tokens_for_user(user)
            return Response({'token':token,'msg':'Registration Successful'},status=status.HTTP_201_CREATED)
        return Response({'msg':serializer.errros},status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    renderer_classes = [UserRenderer]
    def post(self,request,format=None):
        serializer=UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email=serializer.data.get('email')
            password=serializer.data.get('password')
            user=authenticate(request,email=email,password=password)
            if user:
                token = get_tokens_for_user(user)
                return Response({'token':token,"msg":"Login successful"},status=status.HTTP_200_OK)
            else:
                return Response({"errors":{"non_field_errors":['Email or password not valid']}},status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class UserProfileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def get(self,request,format=None):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
class UserChangePasswordView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def post(self,request,format=None):
        serializer = UserChangePasswordSerializer(data=request.data,context={'user':request.user})
        if serializer.is_valid(raise_exception=True):
            return Response({"msg":"Password changed successfully"})
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)