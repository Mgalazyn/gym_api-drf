from django.shortcuts import render
from api.serializers import UserSerializer
from rest_framework import generics
from api.models import User
from api.permissions import AdminPermissions
from rest_framework import viewsets


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer


class UserDetails(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [AdminPermissions]


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return UserSerializer
        return self.serializer_class