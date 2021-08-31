from django.urls import path,re_path
from . import views
urlpatterns = [
    path('image/<uuid:img_id>/', views.image_check, name='image'),
    re_path('username/(?P<user_name>[\u4e00-\u9fa5\w]{3,10})/', views.Username_check.as_view(), name='username'),
    re_path('mobile/(?P<Mobile>1[3-9]\d{9})/', views.Mobile_check.as_view(), name='mobile'),
    path('sms/',views.Sms_code.as_view(),name='sms')
]
