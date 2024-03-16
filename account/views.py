from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import *

# Create your views here.
class UserRegistrationView(APIView):
    def post(self,request,format=None):
        print("Data not input yet")
        serializer=UserRegistrationSerializer(data=request.data)
        print("Data has been input")
        if serializer.is_valid(raise_exception=True):
            print("seri is valid")
            user=serializer.save()
            print('ser is saved')
            return Response({'msg':'Registration Successful'},status=status.HTTP_201_CREATED)
        return Response({'msg':serializer.errros},status=status.HTTP_400_BAD_REQUEST)