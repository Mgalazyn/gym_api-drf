from rest_framework import serializers
from api.models import Exercise


class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = ['name','sets', 'reps', 'weight']
        

class ExerciseDetailsSerializer(ExerciseSerializer):

    class Meta(ExerciseSerializer.Meta):
        fields = ExerciseSerializer.Meta.fields + ['description', 'link']
