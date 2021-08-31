from django.db import models

# Create your models here.
#为django增减手机验证功能，重写Users代码
from django.contrib.auth.models import AbstractUser,UserManager as User_Manager

class UserManager(User_Manager):
    def create_superuser(self, username, password, email=None, **extra_fields):
        return super(UserManager,self).create_superuser(username=username,
                                                        password=password,
                                                        email=email,**extra_fields)

class User(AbstractUser):
    objects = UserManager()
    REQUIRED_FIELDS = ['mobile']
    mobile=models.CharField('手机号',max_length=11,unique=True,
                            error_messages={'unique':'此号码已被注册'})
    emails=models.BooleanField('邮箱状态',default=False)
    class Meta:
        db_table='tbuser'
        verbose_name='用户'
        verbose_name_plural=verbose_name
    def __str__(self):
        return self.username

# from django.conf.global_settings import