from django.urls import path, include
from plan import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('plans', views.PlanViewSet)

app_name = 'plan'

urlpatterns = [
    path('', include(router.urls)),
]