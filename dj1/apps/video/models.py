from django.db import models
from dbapp.base_model import Base_model
# Create your models here.
#讲师表
class Teacher(Base_model):
    name=models.CharField('讲师姓名',max_length=20)
    positional_title=models.CharField('职称',max_length=50)
    profile=models.TextField('讲师简介')
    image_url=models.URLField('头像',default='')

    class Meta:
        db_table='teacher'
        verbose_name='讲师'
        verbose_name_plural=verbose_name

    def __str__(self):
        return self.name

#视频分类表
class Course_category(Base_model):
    name=models.CharField('课程分类',max_length=50)

    class Meta:
        db_table='course_category'
        verbose_name='课程分类'
        verbose_name_plural=verbose_name
    def __str__(self):
        return self.name


#视频课程表
class Course(Base_model):
    title=models.CharField('课程名称',max_length=50)
    cover_url=models.URLField('封面',default='')
    video_url=models.URLField('视频地址',default='')
    profile=models.TextField('课程简介',null=True,blank=True)
    outline=models.TextField('课程大纲',null=True,blank=True)

    teacher=models.ForeignKey('Teacher',on_delete=models.SET_NULL,null=True,blank=True)
    category=models.ForeignKey('Course_category',on_delete=models.SET_NULL,null=True,blank=True)

    class Meta:
        db_table='course'
        verbose_name='课程'
        verbose_name_plural=verbose_name
    def __str__(self):
        return self.title










