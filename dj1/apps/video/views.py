from django.shortcuts import render
from django.views import View
from .models import *
# Create your views here.
#上传视频
class Video_up(View):
    def get(self,request):
        return render(request,'course/video_up.html')



def course(request):
    courses=Course.objects.select_related('teacher','category')\
        .only('title','cover_url','teacher__name','teacher__positional_title','category__name').filter(is_delete=0)
    return render(request,'course/course.html',context={'courses':courses})

def course_detail(request,course_id):
    video=Course.objects.select_related('teacher')\
        .only('title','video_url','profile','outline','teacher__name',
              'teacher__positional_title','teacher__image_url','teacher__profile')\
        .filter(is_delete=0,id=course_id).first()
    return render(request,'course/course_detail.html',context={'video':video})

def search(request):
    return render(request,'news/search.html')



