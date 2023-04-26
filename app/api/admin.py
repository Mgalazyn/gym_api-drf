from django.contrib import admin
from .models import User, Exercise, Plan

# Register your models here.

admin.site.register(User)
admin.site.register(Exercise)
admin.site.register(Plan)