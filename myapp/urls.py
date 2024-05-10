from django.urls import path
from .import views

urlpatterns = [
    path('', views.main, name='main'),
    path('photo/<str:pk>/', views.photo, name='photo'),
    path('deletephoto/<str:pk>/', views.deletephoto, name='deletephoto'),
    path('addphoto/', views.addphoto, name='addphoto'),

    path('loginUser/', views.loginUser, name='loginUser'),
    path('logoutUser/', views.logoutUser, name='logoutUser')
]