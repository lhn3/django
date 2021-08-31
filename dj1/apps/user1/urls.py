from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('register/', views.Register.as_view(), name='register'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('find_pwd/',views.Find_pwd.as_view(),name='find_pwd'),
    path('re_pwd/', views.Re_pwd.as_view(), name='re_pwd'),
]