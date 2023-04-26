from django.shortcuts import render
from api.models import Plan
from rest_framework import viewsets
from plan import serializers

class PlanViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.PlanDetailsSerializer
    queryset = Plan.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.PlanSerializer
        return self.serializer_class
