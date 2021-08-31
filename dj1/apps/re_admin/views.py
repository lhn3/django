from django.shortcuts import render,HttpResponse
from django.views import View
from dbapp.models import *
from files.models import Doc
from django.db.models import Count
from video.models import *
from dj1.response_code import Code,res_json
import json
import time
from dj1.settings.set import IP_PULL
from datetime import datetime
from django.core.paginator import Paginator
from .paginator_self import get_page_data
from six.moves.urllib.parse import urlencode
from dj1.settings.set import FDFS_URL
from fastdfs.fdfs import client
from re_admin.formes import NewsPubForm,DocsPubForm,CourseVideoFrom
import logging
from django.contrib.auth.models import Group,Permission
from user1.models import User
#权限包导入
from django.contrib.auth.mixins import PermissionRequiredMixin,LoginRequiredMixin
from django.contrib.auth.decorators import login_required,permission_required
from django.utils.decorators import method_decorator
logger=logging.getLogger('django')


# Create your views here.

#反爬装饰器
def func(bs):
    def cu_ip(request):
        now_time=time.time()                      #获取请求前的时间
        ip=request.META.get('REMOTE_ADDR')        #获取请求头
        black=request.session.get('blackname')    #查看session
        if ip == black:                           #判断次ip是否被记入session黑名单
            return HttpResponse('超速请求')         #如果有则返回404
        if ip not in IP_PULL:                     #判断次ip是否被记录
            IP_PULL[ip]=[now_time]                #如果没有则记录并记录访问的时间
        history=IP_PULL.get(ip)                   #获取被记录的时间
        while history and now_time-history[-1] >1:#当时间存在和下次访问的时间差大于一定值
            history.pop()                         #删除此ip
        if (len(history)) <5:                     #判断每秒请求小于五次
            history.insert(0,now_time)
            return bs(request)
        else:                                     #如若大于五次
            request.session['blackname']=ip       #要被计入session黑名单
            request.session.set_expiry(120)       #时间2分钟
            return HttpResponse('404')              #并返回404
    return cu_ip


#重写LoginRequiredMixin,登录权限
class Re_LoginRequiredMixin(object):
    @method_decorator(login_required(login_url='/user1/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(Re_LoginRequiredMixin,self).dispatch(request, *args, **kwargs)

# @func
class Admin_index(View):
    def get(self,request):
        return render(request,'admin/index.html')

#分类增改查
class Admin_tags(Re_LoginRequiredMixin,View):
    def get(self,request):  #查
        tags=Tag.objects.values('id','name').annotate(num=Count('news'))\
            .filter(is_delete=0).order_by('-num')     #查id与name并关联查出news表中对应标题的所有新闻赋值给num
        return render(request,'admin/tags.html',context={'tags':tags})
    def post(self,request):  #添加
        Data=request.body
        if not Data:
            return res_json(errno=Code.DATAERR,errmsg='数据错误！')
        Data=json.loads(Data)
        title=Data.get('title')
        title=title.strip()
        if title:
            tag=Tag.objects.get_or_create(name=title) #有返回(obj,False),无返回(obj,True)并写入数据库
            if tag[-1]:
                return res_json(errmsg='标签添加成功！')
            else:
                return res_json(errno=Code.DATAEXIST,errmsg='此标签已存在，请重新输入！')
        else:
            return res_json(errno=Code.NODATA,errmsg='请输入标签名')
    def put(self,request,tag_id):  #改
        data = request.body
        if not data:
            return res_json(errno=Code.DATAERR, errmsg='数据错误！')
        data = json.loads(data)
        title = data.get('title')
        title = title.strip()
        if title:
            res = Tag.objects.filter(name=title).count()
            if res:
                return res_json(errno=Code.DATAEXIST, errmsg='此标签已存在，请重新输入！')
            else:
                Tag.objects.filter(id=tag_id).update(name=title)
                return res_json(errmsg='修改成功！')
        else:
            return res_json(errno=Code.NODATA, errmsg='请输入标签名')


#分类删除
class Admin_deltag(View):
    def post(self,request,tag_id):
        bs=Tag.objects.get(id=tag_id)
        if bs:
            try:
                bs.delete()
                return res_json(errmsg='删除成功')
            except:
                return res_json(errno=Code.SERVERERR,errmsg='删除失败')
        else:
            return res_json(errno=Code.NODATA,errmsg='此标签不存在，删除失败')

#热门新闻
class Admin_hot(View):
    def get(self,request):
        hot=Hotnews.objects.select_related('new__tag','new').only('new__title','priority','new__tag__name')\
            .filter(is_delete=0).order_by('priority')
        return render(request,'admin/hot_news.html',context={'hot':hot})
    def post(self,request):                                  #添加
        data = request.body
        if not data:
            return res_json(errno=Code.DATAERR, errmsg='数据错误！')
        data = json.loads(data)
        priority = data.get('priority')
        news_id=data.get('news_id')

        priority=int(priority)
        news_id=int(news_id)

        if not News.objects.filter(id=news_id).exists():
            return res_json(errno=Code.NODATA,errmsg='未选择文章或文章不存在')
        if priority not in [i for i,_ in Hotnews.CHOICE]:
            return res_json(errno=Code.NODATA,errmsg='请选择正确优先级')

        #创建
        add_hotnews=Hotnews.objects.get_or_create(new_id=news_id,priority=priority)
        if add_hotnews[-1]:
            return res_json(errmsg='热门新闻创建成功')
        else:
            return res_json(errno=Code.DATAEXIST,errmsg='此文章已经是热门新闻，无法重复创建')



    def put(self,request,new_id):                     #改
        data=request.body
        if not data:
            return res_json(errno=Code.DATAERR, errmsg='数据错误！')
        data = json.loads(data)
        new_priority = data.get('new_priority')
        new_priority = int(new_priority)

        priority=[i for i,_ in Hotnews.CHOICE]
        print(priority)
        if new_priority not in priority:
            return res_json(errno=Code.DATAERR,errmsg='优先级输入错误，请重新输入')
        news=Hotnews.objects.only('priority').filter(id=new_id).first()
        print(news,news.priority)
        if not news:
            return res_json(errno=Code.NODATA,errmsg='文章不存在，无法设置优先级')
        if news.priority == new_priority:
            return res_json(errno=Code.DATAEXIST,errmsg='优先级未修改')
        news.priority=new_priority
        news.save(update_fields=['priority'])
        return res_json(errmsg='优先级修改成功')

    def delete(self,request,new_id):
        hotnew=Hotnews.objects.only('id').filter(id=new_id).first()
        if hotnew:
            hotnew.delete()
            # hotnew.is_delete=True
            # hotnew.save(update_fields=['is_delete'])
            return res_json(errmsg='删除成功')
        else:
            return res_json(errno=Code.DATAEXIST,errmsg='文章不存在')

#下拉框选择文章分类对应文章
def tags_select(request):
    tags=Tag.objects.only('name').annotate(num=Count('news')).filter(is_delete=0).order_by('-num')
    priority_dict=Hotnews.CHOICE
    return render(request,'admin/hot_news_add.html',context={'tags':tags,
                                                            'priority_dict':priority_dict})
def news_select(request,sTagId):
    news = News.objects.only('title').filter(is_delete=0, tag=sTagId).order_by('-clicks')
    news_list=[]
    if news:
        for i in news:
            news_list.append({'id': i.id,'title': i.title})
        return res_json(data={'news':news_list})
    else:
        return res_json(errno=Code.NODATA,errmsg='此标签无文章内容')


#文章管理
class Admin_news(View):
    def get(self,request):
        start_time=request.GET.get('start_time','')
        end_time=request.GET.get('end_time','')
        #字符串转日期格式
        start_time=datetime.strptime(start_time,"%Y/%m/%d") if start_time else ''
        end_time=datetime.strptime(end_time,"%Y/%m/%d") if end_time else ''
        #查新闻
        newses=News.objects.select_related('author','tag').only('title','author__username','tag__name','update_time')\
            .filter(is_delete=0)
        #时间过滤
        if start_time and not end_time:
            newses=newses.filter(update_time__gte=start_time)
        if end_time and not start_time:
            newses=newses.filter(update_time__lte=end_time)
        if start_time and end_time:
            newses=newses.filter(update_time__range=[start_time,end_time])
        #题目模糊查询
        title=request.GET.get('title','')
        if title:
            newses=newses.filter(title__icontains=title)
        #作者模糊查询
        author_name=request.GET.get('author_name','')
        if author_name:
            newses=newses.filter(author__username__icontains=author_name)
        #标题查询
        tags=Tag.objects.values('name','id').annotate(num=Count('news')).filter(is_delete=0).order_by('-num')
        tag_id=int(request.GET.get('tag_id',0))
        newses=newses.filter(tag=tag_id) if tag_id else newses
        #分页
        page=int(request.GET.get('page',1))
        pt=Paginator(newses,5)
        try:
            news_info=pt.page(page)
        except:
            news_info=pt.page(pt.num_pages)

        pages_data=get_page_data(pt,news_info)
        #日期格式转字符串

        start_time=start_time.strftime('%Y/%m/%d') if start_time else ''
        end_time=end_time.strftime('%Y/%m/%d') if end_time else ''


        data={'news_info':news_info,
              'tags':tags,
              'start_time':start_time,
              'end_time':end_time,
              'title':title,
              'author_name':author_name,
              'tag_id':tag_id,
              'paginator':pt,
              'other_param': urlencode({
                  'start_time': start_time,
                  'end_time': end_time,
                  'title': title,
                  'author_name': author_name,
                  'tag_id': tag_id,
              })
        }
        data.update(pages_data)
        return render(request,'admin/news.html',context=data)
    def delete(self,request,news_id):
        news = News.objects.only('id').filter(id=news_id).first()
        if news:
            # news.delete()
            news.is_delete=True
            news.save(update_fields=['is_delete'])
            return res_json(errmsg='删除成功')
        else:
            return res_json(errno=Code.DATAEXIST, errmsg='文章不存在')

#文章编辑
class Admin_news_put(View):
    def get(self,request,news_id):
        news=News.objects.select_related('tag').only('title','digest','content','image_url','tag__name')\
            .filter(is_delete=0,id=news_id).first()
        tags=Tag.objects.values('id','name').filter(is_delete=0).annotate(num=Count('news')).order_by("-num")
        return render(request,'admin/news_up.html',context={'news':news,
                                                            'tags':tags})
    def put(self,request,news_id):
        new=News.objects.filter(id=news_id,is_delete=0).first()
        if not new:
            return res_json(errno=Code.PARAMERR,errmsg='此文章不存在')
        news=request.body
        if not news:
            return res_json(errno=Code.PARAMERR,errmsg='参数错误')
        news=json.loads(news)
        #表单验证——————————————————————
        form=NewsPubForm(data=news)
        if form.is_valid():  #返回True，False
            new.title=form.cleaned_data.get('title')
            new.digest=form.cleaned_data.get('digest')
            new.tag=form.cleaned_data.get('tag')
            new.image_url=form.cleaned_data.get('image_url')
            new.content=form.cleaned_data.get('content')
            new.save()
            return res_json(errmsg='文章更新成功')
        else:
            err=[]
            for i in form.errors.values():
                err.append(i[0])
            return res_json(errno=Code.PARAMERR,errmsg=err)


#图片上传到fasrdfs
class Up_image(View):
    def post(self,request):
        name=request.FILES
        file=name.get('image_files') if name.get('image_files') else name.get('text_file') #name.jpg

        if name.get('image_files'):
            if file.content_type not in('image/jpeg','image/gif','image/png'):
                return res_json(errno=Code.PARAMERR,errmsg='只能上传图片文件')
        else:
            if file.content_type not in ('application/zip','application/pdf','text/plain'):
                return res_json(errno=Code.PARAMERR,errmsg='只能上传文档文件')

        #上传到dfs
        up_name=file.name.split('.')[-1]
        try:
            up_img=client.upload_by_buffer(file.read(),file_ext_name=up_name)  #二进制写入并加上后缀名
        except Exception as e:
            logger.error('上传失败{}'.format(e))
            return res_json(errno=Code.UNKOWNERR,errmsg='上传失败')

        if up_img.get('Status') != 'Upload successed.':
            if name.get('image_files'):
                return res_json(errno=Code.UNKOWNERR,errmsg='图片上传失败')
            else:
                return res_json(errno=Code.UNKOWNERR, errmsg='文档上传失败')
        else:
            id=up_img.get('Remote file_id')
            url=FDFS_URL+id
            if name.get('image_files'):
                return res_json(errmsg='图片上传成功',data={'image_url':url})
            else:
                return res_json(errmsg='文档上传成功',data={'text_url':url})


#文章上传
class Admin_news_post(View):
    def get(self,request):
        tags=Tag.objects.values('id','name').filter(is_delete=0).annotate(num=Count('news')).order_by("-num")
        return render(request,'admin/news_up.html',context={'tags':tags})
    def post(self,request,):
        news=request.body
        if not news:
            return res_json(errno=Code.PARAMERR,errmsg='参数错误')
        news=json.loads(news)
        # print(news)
        #表单验证——————————————————————
        form=NewsPubForm(data=news)
        if form.is_valid():  #返回True，False
            if not request.user.is_authenticated:
                return res_json(errno=Code.SESSIONERR, errmsg='请登录后操作')
            news_pu = News.objects.create(title=form.cleaned_data.get('title'))
            news_pu.digest=form.cleaned_data.get('digest')
            news_pu.tag=form.cleaned_data.get('tag')
            news_pu.image_url=form.cleaned_data.get('image_url')
            news_pu.content=form.cleaned_data.get('content')
            news_pu.author_id=request.user.id
            news_pu.save()
            return res_json(errmsg='文章发布成功')
        else:
            err=[]
            for i in form.errors.values():
                err.append(i[0])
            return res_json(errno=Code.PARAMERR,errmsg=err)

#轮播图
class Admin_banner(View):
    def get(self,request):
        banners=Banner.objects.select_related('new').values('id','image_url','priority','new__title','new__id')\
            .filter(is_delete=0).order_by('priority')
        priority_dict=dict(Banner.CHOICE)
        return render(request,'admin/banner.html',context={'priority_dict':priority_dict,
                                                           'banners':banners})
    def delete(self,request,banner_id):
        banner=Banner.objects.filter(is_delete=0,id=banner_id)
        if banner:
            banner.delete()
            # banner.is_delete=True
            # banner.save(update_fields=['is_delete'])
            return res_json(errmsg='删除成功')
        else:
            return res_json(errno=Code.NODATA,errmsg='此文章不存在')
    def put(self,request,banner_id):
        ban=Banner.objects.get(is_delete=0,id=banner_id)
        if not ban:
            return res_json(errno=Code.NODATA,errmsg='轮播图不存在')
        data=request.body
        if not data:
            return res_json(errno=Code.NODATA,errmsg='参数错误')
        data=json.loads(data)
        priority=int(data.get('priority'))
        img_url=data.get('img_url')
        priority_list=[i for i,_ in Banner.CHOICE]       #[1,2,3,4,5,6]
        if priority not in priority_list:
            return res_json(errno=Code.NODATA,errmsg='优先级不存在')
        if not img_url:
            return res_json(errno=Code.NODATA,errmsg='请选择图片')
        if priority==ban.priority and img_url==ban.image_url:
            return res_json(errno=Code.DATAEXIST,errmsg='数未修改，无需更新')
        print(ban.priority,ban.image_url,type(ban.priority))
        ban.priority=priority
        ban.image_url=img_url
        ban.save(update_fields=['priority','image_url'])
        return res_json(errmsg='更新成功')


#添加轮播图
class Admin_banner_post(View):
    def get(self,request):
        tags=Tag.objects.values('id','name').annotate(num=Count('news')).filter(is_delete=0).order_by('-num')
        priority=dict(Banner.CHOICE)
        return render(request,'admin/banner_post.html',context={'tags':tags,
                                                              'priority_dict':priority})
    def post(self,request):
        data=request.body
        if not data:
            return res_json(errno=Code.PARAMERR, errmsg='参数错误')
        data=json.loads(data)
        img_url =data.get('image')
        tag_id = int(data.get('tag'))
        news_id = int(data.get('news'))
        priority = int(data.get('priority'))

        if not img_url:
            return res_json(errno=Code.NODATA,errmsg='请选择图片')
        if not tag_id:
            return res_json(errno=Code.NODATA,errmsg='请选择文章分类')
        if not news_id:
            return res_json(errno=Code.NODATA,errmsg='请选择文章')
        if priority not in [i for i,_ in Banner.CHOICE]:
            return res_json(errno=Code.NODATA,errmsg='请正确选择优先级')

        news=Banner.objects.values('new_id')
        if news_id in [j['new_id'] for j in news]:
            return res_json(errno=Code.DATAEXIST,errmsg='此文章已设置为轮播图，不可重复设置')
        Banner.objects.create(new_id=news_id,priority=priority,image_url=img_url)
        return res_json(errmsg='上传成功')


#文档
class Admin_docs(View):
    def get(self,request):
        docs=Doc.objects.only('title','update_time','create_time','author','file_url')\
            .filter(is_delete=0)
        return render(request,'admin/docs.html',context={'docs':docs})
    def delete(self,request,doc_id):
        doc=Doc.objects.get(id=doc_id,is_delete=0)
        if doc:
            doc.delete()
            return res_json(errmsg='删除成功！')
        else:
            return res_json(errno=Code.NODATA, errmsg='文档不存在，无需删除')

#文档更新
class Admin_docs_put(View):
    def get(self,request,doc_id):
        doc=Doc.objects.only('title','file_url','image_url','desc')\
            .filter(is_delete=0,id=doc_id).first()
        return render(request,'admin/docs_put_post.html',context={'doc':doc})
    def put(self,request,doc_id):
        doc=Doc.objects.filter(id=doc_id,is_delete=0).first()
        if not doc:
            return res_json(errno=Code.NODATA,errmsg='此文档已不存在，更新失败！')
        data=request.body
        if not data:
            return res_json(errno=Code.NODATA,errmsg='参数错误')
        data=json.loads(data)
        form=DocsPubForm(data=data)
        if form.is_valid():
            for i,j in form.cleaned_data.items():
                setattr(doc,i,j)
            doc.save()
            return res_json(errmsg='更新成功')
        else:
            err=[]
            for i in form.errors.values():
                err.append(i[0])
            return res_json(errno=Code.PARAMERR,errmsg=err)

#上传新文档
class Admin_docs_post(View):
    def get(self,request):
        return render(request, 'admin/docs_put_post.html')
    def post(self,request):
        data = request.body
        if not data:
            return res_json(errno=Code.NODATA, errmsg='参数错误')
        data = json.loads(data)
        form = DocsPubForm(data=data)
        if form.is_valid():
            if not request.user.is_authenticated:
                return res_json(errno=Code.SESSIONERR, errmsg='请登录后操作')
            doc=form.save(commit=False)         #form.save()可直接提交传过来的数据建立一条新的数据,先不提交并创建一个对象保存author
            doc.author_id=request.user.id
            doc.save()
            return res_json(errmsg='更新成功')
        else:
            err = []
            for i in form.errors.values():
                err.append(i[0])
            return res_json(errno=Code.PARAMERR, errmsg=err)


#视频展示
class Admin_video(View):
    def get(self,request):
        courses=Course.objects.select_related('teacher','category')\
            .only('title','teacher__name','category__name').filter(is_delete=0).order_by('update_time')
        return render(request,'admin/video.html',context={'courses':courses})
    def delete(self,request,v_id):
        video=Course.objects.filter(is_delete=0,id=v_id).first()
        if v_id:
            video.delete()
            return res_json(errmsg='删除成功！')
        else:
            return res_json(errno=Code.NODATA,errmsg='文章不存在，删除失败！')


#视频课程更新
class Admin_video_put(View):
    def get(self,request,v_id):
        course=Course.objects.only('title','cover_url','video_url','profile','outline','teacher','category')\
            .filter(is_delete=0,id=v_id).first()
        teachers=Teacher.objects.only('name').filter(is_delete=0)
        categories=Course_category.objects.only('name').filter(is_delete=0)
        return render(request,'admin/video_put_post.html',context={'course':course,
                                                                   'teachers':teachers,
                                                                   'categories':categories})
    def put(self,request,v_id):
        video=Course.objects.filter(is_delete=0,id=v_id).first()
        if not video:
            return res_json(errno=Code.NODATA,errmsg='此课程不存在，更新失败！')
        data=request.body
        if not data:
            return res_json(errno=Code.NODATA,errmsg='参数错误！')
        data=json.loads(data)
        form=CourseVideoFrom(data=data)
        if form.is_valid():
            for i,j in form.cleaned_data.items():
                setattr(video,i,j)
            video.save()
            return res_json(errmsg='更新成功')
        else:
            err = []
            for i in form.errors.values():
                err.append(i[0])
            return res_json(errno=Code.PARAMERR, errmsg=err)

#视频课程添加

class Admin_video_post(View):
    def get(self,request):
        teachers = Teacher.objects.only('name').filter(is_delete=0)
        categories = Course_category.objects.only('name').filter(is_delete=0)
        return render(request,'admin/video_put_post.html',context={'teachers':teachers,
                                                                   'categories':categories})
    def post(self,request):
        data=request.body
        if not data:
            return res_json(errno=Code.NODATA,errmsg='参数错误！')
        data=json.loads(data)
        form=CourseVideoFrom(data=data)
        if form.is_valid():
            if not request.user.is_authenticated:
                return res_json(errno=Code.SESSIONERR, errmsg='请登录后操作')
            video=form.save(commit=False)
            video.save()
            return res_json(errmsg='更新成功')
        else:
            err = []
            for i in form.errors.values():
                err.append(i[0])
            return res_json(errno=Code.PARAMERR, errmsg=err)

#用户组管理
class Admin_usergroup(View):
    def get(self,request):
        groups=Group.objects.values('id','name').annotate(num=Count('user'))\
            .order_by('-num')
        return render(request,'admin/user/group_user.html',context={'groups':groups})
    def delete(self,request,group_id):
        group=Group.objects.filter(id=group_id).first()
        if group:
            group.delete()
            return res_json(errmsg='删除成功！')
        else:
            return res_json(errno=Code.NODATA,errmsg='数据不存在，删除失败！')


#已有的用户组设权
class Admin_usergroup_put(View):
    def get(self,request,group_id):
        group=Group.objects.filter(id=group_id).first()
        permissions=Permission.objects.all()
        return render(request,'admin/user/group_user_power.html',context={'group':group,
                                                                          'permissions':permissions})
    def put(self,request,group_id):
        group=Group.objects.filter(id=group_id).first()
        if not group:
            return res_json(errno=Code.NODATA,errmsg='此分组不存在，无法修改！')
        power=request.body
        if not power:
            return res_json(errno=Code.NODATA,errmsg='参数错误！')
        power=json.loads(power)

        Name=power.get('name').strip()
        permission=power.get('permissions')                 #字典
        permissions=set(int(i) for i in permission)              #去重
        if not Name:
            return res_json(errno=Code.NODATA,errmsg='组名不能为空！')
        if Name != group.name and Group.objects.filter(name=Name).exists():
            return res_json(errno=Code.DATAEXIST,errmsg='组名已存在，请重新填写！')
        if not permissions:
            return res_json(errno=Code.NODATA,errmsg='至少选择一个权限')

        old_permissions=set(j for j in group.permissions.all()) #查更改前的权限
        if permissions==old_permissions and Name==group.name:
            return res_json(errno=Code.DATAEXIST,errmsg='未作修改，无需更新！')

        all_permissions=set(s.id for s in Permission.objects.only('id'))
        if not permissions.issubset(all_permissions):           #判断传来的权限是否是所有权限的子集
            return res_json(errno=Code.NODATA,errmsg='权限有误，请重新选择！')

        group.permissions.clear()                           #清楚之前的所有权限
        #遍历并保存
        for w in permission:
            w=int(w)
            p=Permission.objects.get(id=w)
            group.permissions.add(p)
        group.name=Name
        group.save()
        return res_json(errmsg='更新成功')


# 新建用户组并设权
class Admin_usergroup_post(View):
    def get(self,request):
        permissions = Permission.objects.all()
        return render(request, 'admin/user/group_user_power.html', context={'permissions': permissions})
    def post(self,request):
        power = request.body
        if not power:
            return res_json(errno=Code.NODATA, errmsg='参数错误！')
        power = json.loads(power)

        Name = power.get('name').strip()
        permission = power.get('permissions')  # 字典
        permissions = set(int(i) for i in permission)  # 去重
        if not Name:
            return res_json(errno=Code.NODATA, errmsg='组名不能为空！')

        group,ex=Group.objects.get_or_create(name=Name) #有返回（对象，false），无返回（对象，true）
        if not ex: #返回true，false
            return res_json(errno=Code.DATAEXIST, errmsg='组名已存在，请重新填写！')
        if not permissions:
            return res_json(errno=Code.NODATA, errmsg='至少选择一个权限')

        all_permissions = set(s.id for s in Permission.objects.only('id'))
        if not permissions.issubset(all_permissions):       # 判断传来的权限是否是所有权限的子集
            return res_json(errno=Code.NODATA, errmsg='权限有误，请重新选择！')

        # 遍历并保存
        for w in permission:
            w = int(w)
            p = Permission.objects.get(id=w)
            group.permissions.add(p)
        group.name = Name
        group.save()
        return res_json(errmsg='更新成功')

#用户管理

class Admin_users(View):
    def get(self,request):
        users=User.objects.only('username','is_staff','is_superuser','groups__name').filter(is_active=1)
        return render(request,'admin/user/users.html',context={'users':users})
    def delete(self,request,user_id):
        user=User.objects.filter(id=user_id,is_active=1).first()
        if user:
            user.groups.clear()                 #清除组
            user.user_permissions.clear()       #清除权限
            user.is_active=False
            user.save()
            return res_json(errmsg='删除成功！')
        else:
            return res_json(errno=Code.NODATA,errmsg='此用户不存在，无需删除！')


class Ademin_users_put(View):
    def get(self,request,user_id):
        user_instance=User.objects.only('username','is_staff','is_superuser','groups__name')\
            .filter(is_active=1,id=user_id).first()
        groups=Group.objects.only('name')
        return render(request,'admin/user/users_edit.html',context={'user_instance':user_instance,
                                                                    'groups':groups})

    def put(self,request,user_id):
        user=User.objects.filter(id=user_id,is_active=1).first()
        if not user:
            return res_json(errno=Code.NODATA,errmsg='用户不存在，更新失败！')
        data=request.body
        if not data:
            return res_json(errno=Code.NODATA,errmsg='参数错误！')

        data=json.loads(data)
        is_staff=int(data.get('is_staff'))
        is_superuser=int(data.get('is_superuser'))
        is_active=int(data.get('is_active'))
        groups=data.get('groups')

        par=[is_staff,is_superuser,is_active]
        if not all([i in [0,1] for i in par]):          #判断三个参数是否都是为1或0
            return res_json(errno=Code.NODATA,errmsg='参数有误！')
        if not groups:
            return res_json(errno=Code.NODATA, errmsg='请选择分组！')
        groups=set(int(i) for i in groups)
        all_group=set(i.id for i in Group.objects.only('id'))
        if not groups.issubset(all_group):
            return res_json(errno=Code.PARAMERR,errmsg='存在未知分组，更新失败！')

        #保存
        g=Group.objects.filter(id__in=groups)     #查出id在选择的组中的对象（多个对象）
        user.groups.clear()
        user.is_staff=bool(is_staff)
        user.is_superuser=bool(is_superuser)
        user.is_active=bool(is_active)
        user.groups.set(g)                             #关联表中以对象方式保存
        user.save()
        return res_json(errmsg='更新成功')




