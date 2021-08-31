from django.urls import path
from . import views
urlpatterns = [
    path('video_up/', views.Video_up.as_view(), name='video_up'),
    path('course/', views.course, name='course'),
    path('course_detail/<int:course_id>/', views.course_detail, name='course_detail'),
    path('search/', views.search, name='search'),
]