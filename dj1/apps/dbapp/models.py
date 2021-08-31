from django.db import models
from .base_model import Base_model
# Create your models here.

# - 文章分类表： name     create_time  update_time   is_delete
# - 文章表： title  digest  content   clicks   image_url    author(一对错多)   tag(一对多关系)
# - 文章评论表：content   author(一对多关系)   news()
# - 热门文章表：news(一对一)   pirority
# - 轮播图表： image_url   pirority    news(一对一)

#文章分类表
class Tag(Base_model):
    name=models.CharField(max_length=64,verbose_name='标签名')
    class Meta:
        ordering=['-update_time','id']
        db_table='tag'
        verbose_name='文章分类'
        verbose_name_plural=verbose_name
    def __str__(self):
        return self.name

#文章表
class News(Base_model):
    title=models.CharField(max_length=200,verbose_name='标题')
    digest=models.CharField(max_length=200,verbose_name='摘要')
    content=models.TextField(verbose_name='内容')
    clicks=models.IntegerField(default=0,verbose_name='点击量')
    image_url=models.URLField(default='',verbose_name='图片')
    tag=models.ForeignKey('Tag',on_delete=models.SET_NULL,null=True)
    author=models.ForeignKey('user1.User',on_delete=models.SET_NULL,null=True)
    class Meta:
        ordering=['-update_time','id']
        db_table='news'
        verbose_name='文章新闻'
        verbose_name_plural=verbose_name
    def __str__(self):
        return self.title

# 文章评论表
class Comments(Base_model):
    content=models.TextField(verbose_name='评论内容')
    author=models.ForeignKey('user1.User',on_delete=models.SET_NULL,null=True)
    new=models.ForeignKey('News',on_delete=models.CASCADE)
    parent=models.ForeignKey('self',on_delete=models.CASCADE,null=True)

    class Meta:
        ordering=['-update_time','id']
        db_table='comments'
        verbose_name='评论'
        verbose_name_plural=verbose_name
    def comments_dict(self):
        comment_dict={
            'new_id':self.new.id,
            'content_id':self.id,
            'content':self.content,
            'author':self.author.username,
            'update_time':self.update_time,
            'parent':self.parent.comments_dict() if self.parent else None
        }
        return comment_dict
    def __str__(self):
        return '评论{}'.format(self.id)

#热门文章表
class Hotnews(Base_model):
    CHOICE=[
        (1, '第一级'),
        (2, '第二级'),
        (3, '第三级'),
    ]
    new=models.OneToOneField('News',on_delete=models.CASCADE)
    priority=models.IntegerField(verbose_name='优先级',choices=CHOICE)
    class Meta:
        ordering=['-update_time','id']
        db_table='hotnews'
        verbose_name='热门新闻'
        verbose_name_plural=verbose_name
    def __str__(self):
        return '热门新闻{}'.format(self.id)

#轮播图
class Banner(Base_model):
    CHOICE = [
        (1, '第一级'),
        (2, '第二级'),
        (3, '第三级'),
        (4, '第四级'),
        (5, '第五级'),
        (6, '第六级'),
    ]
    image_url=models.URLField(default='',verbose_name='轮播图片url')
    priority=models.IntegerField(verbose_name='优先级',choices=CHOICE)
    new=models.OneToOneField('News',on_delete=models.CASCADE)
    class Meta:
        ordering=['priority','-update_time','id']
        db_table='banner'
        verbose_name='轮播图'
        verbose_name_plural=verbose_name
    def __str__(self):
        return '轮播图{}'.format(self.id)

