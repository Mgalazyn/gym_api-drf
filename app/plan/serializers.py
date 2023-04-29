from rest_framework import serializers
from api.models import Plan, Exercise
from exercise.serializers import ExerciseSerializer



class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ['name']


class PlanDetailsSerializer(PlanSerializer):
    class Meta(PlanSerializer.Meta):
        fields = PlanSerializer.Meta.fields + ['exercises']