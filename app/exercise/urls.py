from django.urls import path, include
from exercise import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('exercises', views.ExerciseViewSet)
router.register('tags', views.TagViewSet)

app_name = 'exercise'

urlpatterns = [
    path('', include(router.urls)),
]