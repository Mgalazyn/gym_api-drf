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

    def _get_or_create_tags(self, tag, exercise):
        """Handle getting or creating tags as needed."""
        for t in tag:
            tag_obj, created = Tag.objects.get_or_create(
                **t,
            )
            exercise.tag.add(tag_obj)

    def create(self, validated_data):
        """Create a exercise."""
        tag = validated_data.pop('tag')
        exercise = Exercise.objects.create(**validated_data)
        self._get_or_create_tags(tag, exercise)

        return exercise
    
    def update(self, instance, validated_data):
        tag = validated_data.pop('tag', None)
        if tag is not None:
            instance.tag.clear()
            self._get_or_create_tags(tag, instance)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return 
    
class ExerciseDetailsSerializer(ExerciseSerializer):

    class Meta(ExerciseSerializer.Meta):
        fields = ExerciseSerializer.Meta.fields + ['description', 'link']

