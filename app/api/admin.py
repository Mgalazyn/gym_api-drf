from django.contrib import admin
from .models import User, Exercise, Plan, Tag

# Register your models here.

admin.site.register(User)
admin.site.register(Exercise)
admin.site.register(Plan)
admin.site.register(Tag)