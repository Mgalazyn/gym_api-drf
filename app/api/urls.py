from django.urls import path
from api import views

app_name = 'user'

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('update/<str:pk>/', views.UserDetails.as_view(), name='update-user')
]