from rest_framework import serializers
from api.models import Exercise, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']
        read_only_fields = ['id']
        

class ExerciseSerializer(serializers.ModelSerializer):
    tag = TagSerializer(many=True, required=False)

    class Meta:
        model = Exercise
        fields = ['name','sets', 'reps', 'weight', 'tag']


class ExerciseDetailsSerializer(ExerciseSerializer):

    class Meta(ExerciseSerializer.Meta):
        fields = ExerciseSerializer.Meta.fields + ['description', 'link']

    # def create(self, validated_data):
    #     tag_data = validated_data.pop('tag')
    #     exercise = Exercise.objects.create(**validated_data)
    #     for t_data in tag_data:
    #         Exercise.objects.create(exercise, **t_data)
    #     return exercise