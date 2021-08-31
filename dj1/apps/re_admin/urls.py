from django.urls import path,include,re_path
from django.views.static import serve
from . import views
urlpatterns = [
    path('admin_index/', views.Admin_index.as_view(), name='admin_index'),
    path('admin_tags/', views.Admin_tags.as_view(), name='admin_tags'),
    path('admin_retag/<int:tag_id>/', views.Admin_tags.as_view(), name='admin_retag'),
    path('admin_deltag/<int:tag_id>/', views.Admin_deltag.as_view(), name='admin_deltag'),

    path('admin_hot/', views.Admin_hot.as_view(), name='admin_hot'),
    path('admin_rehot/<int:new_id>/', views.Admin_hot.as_view(), name='admin_rehot'),
    path('admin_delhot/<int:new_id>/', views.Admin_hot.as_view(), name='admin_delhot'),

    path('admin_addhot/', views.tags_select,name='admin_addhot'),
    path('news_select/<int:sTagId>/', views.news_select),

    path('admin_news/', views.Admin_news.as_view(),name='admin_news'),
    path('admin_delnews/<int:news_id>/', views.Admin_news.as_view(), name='admin_delnews'),

    path('admin_news_put/<int:news_id>/', views.Admin_news_put.as_view(), name='admin_news_put'), #文章更新

    path('news/img_dfs/', views.Up_image.as_view(), name='img_dfs'),   #图片上传dfs

    path('admin_news_post/', views.Admin_news_post.as_view(), name='admin_news_post'),  # 文章上传

    path('admin_banner/', views.Admin_banner.as_view(), name='admin_banner'),  # 轮播图查看
    path('admin_banner_del/<int:banner_id>/', views.Admin_banner.as_view(), name='admin_banner_del'),  # 轮播图删除
    path('admin_banner_put/<int:banner_id>/', views.Admin_banner.as_view(), name='admin_banner_put'),  # 轮播图编辑
    path('admin_banner_post/', views.Admin_banner_post.as_view(), name='admin_banner_post'),  # 轮播图添加

    path('admin_docs/', views.Admin_docs.as_view(), name='admin_docs'),  # 文档
    path('admin_docs_put/<int:doc_id>/', views.Admin_docs_put.as_view(), name='admin_docs_put'),  # 文档编辑
    path('admin_docs_del/<int:doc_id>/', views.Admin_docs.as_view(), name='admin_docs_del'),  # 文档删除
    path('admin_docs_post/', views.Admin_docs_post.as_view(), name='admin_docs_post'),  # 文档上传

    path('admin_video/', views.Admin_video.as_view(), name='admin_video'),  # 视频
    path('admin_video_put/<int:v_id>/', views.Admin_video_put.as_view(), name='admin_video_put'),  # 视频课程更新
    path('admin_video_del/<int:v_id>/', views.Admin_video.as_view(), name='admin_video_del'),  # 视频课程删除
    path('admin_video_post/', views.Admin_video_post.as_view(), name='admin_video_post'),  # 视频课程添加

    path('admin_usergroup/', views.Admin_usergroup.as_view(), name='admin_usergroup'),  # 用户组管理
    path('admin_usergroup_put/<int:group_id>/', views.Admin_usergroup_put.as_view(), name='admin_usergroup_put'),  # 已有的用户组设权
    path('admin_usergroup_del/<int:group_id>/', views.Admin_usergroup.as_view(), name='admin_usergroup_del'),  # 已有的用户组删除
    path('admin_usergroup_post/', views.Admin_usergroup_post.as_view(), name='admin_usergroup_post'),  # 新建用户组并设权

    path('admin_users/', views.Admin_users.as_view(), name='admin_users'),  # 用户管理
    path('admin_users_del/<int:user_id>/', views.Admin_users.as_view(), name='admin_users_del'),  # 用户管理
    path('admin_users_put/<int:user_id>/', views.Ademin_users_put.as_view(), name='admin_users_put'),  # 用户权限编辑

]