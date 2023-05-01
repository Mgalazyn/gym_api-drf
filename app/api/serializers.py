from django.contrib.auth import get_user_model
from rest_framework import serializers
import re
from api.models import Exercise, User, Tag


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'name']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 8}}

    def create(self, validated_data):
        password = validated_data.get('password')
        if not re.search(r'\d.*\d.*\d', password):
            raise serializers.ValidationError('Password must contain at least 3 digits.')
        user = get_user_model().objects.create_user(**validated_data)
        return user
    

    def update(self, instance, validated_data):
        #update user 
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()
        
        return user
    
class UserImageSerializer(serializers.ModelSerializer):
    #serializer for uploading images for user

    class Meta:
        model = User
        fields = ['id', 'image']
        read_only_fields = ['id']
        extra_kwargs = {'image': {'required': 'True'}}


class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'name', 'image']


