from django.db import models
from django.contrib.auth.models import (AbstractBaseUser,
                                        BaseUserManager,
                                        PermissionsMixin)
from django.core.validators import validate_email
import uuid
import os


def user_image_file_path(instance, filename):
    #genereating file path for user image
    ext = os.path.splitext(filename)[1]
    filename = f'{uuid.uuid4()}{ext}'

    return os.path.join('uploads', 'user', filename)


class UserManager(BaseUserManager):
    #Method for creating users 
    def create_user(self, email, password=None, **extra_fields):
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    #Custom user model
    email = models.EmailField(max_length=250, unique=True, blank=False, null=False, validators=[validate_email])
    name = models.CharField(max_length=250)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    image = models.ImageField(null=True, upload_to=user_image_file_path)

    objects = UserManager()
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email


class Exercise(models.Model):
    #Exercise object
    name = models.CharField(max_length=255)
    sets = models.PositiveIntegerField()
    reps = models.PositiveIntegerField()
    weight = models.CharField(max_length=50)
    description = models.TextField(max_length=500, null=True, blank=True)
    link = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name


class Plan(models.Model):
    name = models.CharField(max_length=255)
    exercises = models.ManyToManyField('Exercise')

    def __str__(self):
        return self.name