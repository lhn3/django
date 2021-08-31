from django.shortcuts import render,Http404
from .models import *
from django.views import View
from django.db.models import F
from django.core.paginator import Paginator
from dj1.response_code import res_json,Code
import logging
from django.core import serializers
import json
from django.contrib.auth.decorators import login_required
logger=logging.getLogger('django')
# Create your views here.

# @login_required(login_url='/user1/login/')
def index(request):
    tags=Tag.objects.filter(is_delete=0).only('name')
    click_news=News.objects.select_related('author','tag')\
        .only('title','image_url','update_time','tag__name','author__username','digest')\
        .filter(is_delete=0).order_by('-clicks')[0:3]
    hot_news=Hotnews.objects.select_related('new').only('new__title','new__image_url')\
        .filter(is_delete=0).order_by('priority')
    # click=News.objects.filter(is_delete=0).order_by('-clicks')[0]
    # click.title='python的序列与映射的解包操作'
    # click.save()
    return render(request,'news/index.html',context={'tags':tags,
                                                     'click_news':click_news,
                                                     'hot_news':hot_news})
#文章内容列
class NewsList(View):
    def get(self,request):
        try:
            tag_id=int(request.GET.get('tag_id',0))
        except Exception as e:
            logger.info('页面标签定义错误{}'.format(e))
        try:
            page=int(request.GET.get('page',1))
        except Exception as e:
            logger.info('页码定义错误{}'.format(e))
            page=1
        news_list=News.objects.values('title','digest','image_url','update_time','id').annotate\
            (tag_name=F('tag__name'),author=F('author__username'))

        news=news_list.filter(is_delete=False,tag_id=tag_id) or news_list.filter(is_delete=False)

        p=Paginator(news,5)
        try:
            news_info=p.page(page)
        except Exception as e:
            news_info=p.page(p.num_pages)
            logger.info(news_info,e)
        data={
            'news':list(news_info),
            'total_pages':p.num_pages
        }
        return res_json(data=data)

# 文章内容
class NewsDetail(View):
    def get(self,request,news_id):
        news_detail=News.objects.select_related('author','tag')\
            .only('title','update_time','author__username','tag__name','content').filter(id=news_id).first()

        comments=Comments.objects.select_related('author','parent')\
            .only('author__username','content','update_time','parent__update_time')\
            .filter(is_delete=0,new_id=news_id)

        comments_list=[]
        for i in comments:
            comments_list.append(i.comments_dict())

        if news_detail:
            news_detail.clicks += 1
            news_detail.save(update_fields=['clicks'])
            return render(request,'news/news_detail.html',context={'news_detail':news_detail,
                                                                   'comments':comments_list})
        else:
            return Http404('错误请求')

# 轮播图
class Banners(View):
    def get(self,request):
        ban=Banner.objects.select_related('new').only('image_url','new__title',)\
            .filter(is_delete=0).order_by('priority')
        banners=[]
        for i in ban:
            banners.append(
                {
                    'news_id':i.new.id,
                    'image_url':i.image_url,
                    'news_title':i.new.title
                })
        data={
            'banners':banners
        }
        return res_json(data=data)

#评论追加
class CommentsView(View):
    def post(self,request,news_id):
        if not request.user.is_authenticated:
            return res_json(errno=Code.SESSIONERR,errmsg='请登录后操作')
        if not News.objects.filter(is_delete=False,id=news_id).exists():
            return res_json(errno=Code.PARAMERR,errmsg='文章不存在')
        data=request.body
        data=json.loads(data)
        if not data:
            return res_json(errno=Code.PARAMERR,errmsg='参数错误')
        content=data.get('content')
        if not content:
            return res_json(errno=Code.PARAMERR,errmsg='请输入评论内容')
        parent_id=data.get('parent_id')
        if parent_id:
            if not Comments.objects.filter(is_delete=False,id=parent_id,new_id=news_id):
                return res_json(errno=Code.PARAMERR,errmsg='错误评论')

        news_content = Comments()
        news_content.content = content
        news_content.new_id = news_id
        news_content.author = request.user
        news_content.parent_id = parent_id if parent_id else None
        news_content.save()
        return res_json(data=news_content.comments_dict())


