from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth.hashers import make_password
from .serializers import SingUpSerializer, UserSerializer

from django.contrib.auth.models import User
# Create your views here.


@api_view(['POST'])
def register(request):
    data = request.data
    user = SingUpSerializer(data=data)

    if user.is_valid():
        if not User.objects.filter(email=data['email']).exists():

            user = User.objects.create(
                first_name=data['first_name'],
                last_name=data['last_name'],
                email=data['email'],
                username=data['email'],
                password=make_password(data['password'])
            )
            return Response(
                {"message": "User created successfully"},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)

    else:
        return Response(user.errors, status=status.HTTP_400_BAD_REQUEST)
