from celery import Celery
import os

if not os.getenv('DJANGO_SETTINGS_MODULE'):
    os.environ['DJANGO_SETTINGS_MODULE']='dj1.settings.set'

celery_app=Celery('smses')                           #创建实例
celery_app.config_from_object('celery_tasks.config') #加载配置
celery_app.autodiscover_tasks(['celery_tasks.sms'])  #注册任务

