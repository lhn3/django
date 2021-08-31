from django.db import models

class Base_model(models.Model):
    create_time=models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    update_time=models.DateTimeField(auto_now=True,verbose_name='更新时间')
    is_delete=models.BooleanField(default=False,verbose_name='逻辑删除')
    class Meta:
        abstract=True #为抽象模型，用于其他模型继承，数据库迁移不会创建表格