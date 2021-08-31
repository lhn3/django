from django.urls import path
from . import views
urlpatterns = [
    path('index/', views.index, name='index'),
    path('news/', views.NewsList.as_view(), name='news'),
    path('news_detail/<int:news_id>/', views.NewsDetail.as_view(), name='news_detail'),
    path('banner/', views.Banners.as_view(), name='banner'),
    path('news/<int:news_id>/comments/', views.CommentsView.as_view(), name='comments'),
]