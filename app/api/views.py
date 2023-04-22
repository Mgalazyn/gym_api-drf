from django.shortcuts import render
from api.serializers import UserSerializer
from rest_framework import generics
from api.models import User
from api.permissions import AdminPermissions


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer


class UserDetails(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [AdminPermissions]

