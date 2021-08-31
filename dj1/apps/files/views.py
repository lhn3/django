from django.shortcuts import render
from .models import *
import requests
from django.http import Http404,FileResponse
from django.utils.encoding import escape_uri_path
# Create your views here.
def doc(request):
    docs=Doc.objects.only('title','desc','image_url','file_url').filter(is_delete=0)
    return render(request,'doc/docDownload.html',context={'docs':docs})

def download_doc(request,doc_id):
    file=Doc.objects.only('file_url').filter(is_delete=0,id=doc_id).first()
    if file:
        file=file.file_url
        url='http://127.0.0.1:8000'+file
        res=FileResponse(requests.get(url))
        name=url.split('.')[-1]              #取出后缀
        print(name)

        if not name:
            return Http404('文件名异常')
        else:
            name=name.lower()

        if name=='pdf':                             #获取不同文件的不同下载方式
            res['Content-type']='application/pdf'
        elif name=='doc':
            res['Content-type']='application/msowrd'
        elif name=='ppt':
            res['Content-type']='application/powerpoint'
        else:
            raise Http404('文件格式错误')

        fail_name=escape_uri_path(url.split('/')[-1])  #设置下载后的文件的名字

        res['Content-Disposition']="attachment;filename*=UTF-8''{}".format(fail_name)
        return res
    else:
        raise Http404('文档不存在')






