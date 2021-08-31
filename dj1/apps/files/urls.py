from django.urls import path
from . import views
urlpatterns = [
    path('doc/', views.doc, name='doc'),
    path('download_doc/<int:doc_id>/', views.download_doc, name='download_doc')
]