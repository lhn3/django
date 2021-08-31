from django.db import models
from dbapp.base_model import Base_model
# Create your models here.

class Doc(Base_model):
    file_url=models.URLField('文件url')
    title=models.CharField('文档标题',max_length=100)
    desc=models.TextField('文件描述')
    image_url=models.URLField('图片url',default='')
    author=models.ForeignKey('user1.User',on_delete=models.SET_NULL,null=True)
    class Meta:
        db_table='docs'
        verbose_name='在线文档'
        verbose_name_plural=verbose_name
    def __str__(self):
        return self.title



