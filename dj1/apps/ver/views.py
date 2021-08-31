from django.shortcuts import render,HttpResponse
from django_redis import get_redis_connection
from django.views.generic import View
from django.http import JsonResponse
from captcha.captcha import captcha
from user1.models import User
from dj1.response_code import res_json,Code
import json,random
from celery_tasks.sms.tasks import send_sms
# from yuntongxun.sms import CCP
# Create your views here.
def image_check(request,img_id):
    text,image=captcha.generate_captcha()
    conntent_redis=get_redis_connection('verify')
    conntent_redis.setex('img_{}'.format(img_id).encode('utf8'),120,text)

    # request.session['image_code']=text
    # request.session.set_expiry(60*2)
    # print(request.session.values())
    # print(request.session.get('image_code'))
    print(text,img_id)
    return HttpResponse(content=image,content_type='image/jpg')

class Username_check(View):
    def get(self,request,user_name):
        count=User.objects.filter(username=user_name).count()
        data={'count':count}
        # return JsonResponse(data=data)
        return res_json(data=data)

class Mobile_check(View):
    def get(self,request,Mobile):
        count=User.objects.filter(mobile=Mobile).count()
        data={'count':count}
        # return JsonResponse(data=data)
        return res_json(data=data)

class Sms_code(View):
    def post(self,request):
        bs=request.body  #获取前端传来的Data（json格式）
        Data=json.loads(bs)
        text=Data.get('text')
        mobile=Data.get('mobile')
        uuid=Data.get('uuid')
        p=Data.get('p')
        conntent_redis=get_redis_connection('verify')#连接redis数据库

        # 检查有没有重复发送手机短信
        send_flag=conntent_redis.get('smsflag_{}'.format(mobile))
        if send_flag:
            return res_json(errno=Code.DATAEXIST,errmsg='短信发送频繁')

        # 验证验证码
        if p == '1':
            image_text=conntent_redis.get('img_{}'.format(uuid))
            if image_text is None:
                return res_json(errno=Code.PARAMERR,errmsg='验证码过期，请刷新')
            try:
                conntent_redis.delete('img_{}'.format(uuid))  #删除验证码数据
            except:
                pass
            image_text=image_text.decode()
            if text.lower() != image_text.lower():
                return res_json(errno=Code.PARAMERR,errmsg='验证码错误，请重新输入')

        # 发送短信
        smses='%06d'%random.randint(0,999999)
        print(smses)
        conntent_redis.setex('sms_{}'.format(mobile),300,smses) #验证码写入redis
        conntent_redis.setex('smsflag_{}'.format(mobile),60,1)  #标记此号码1分钟内发过短信

        # ccp=CCP()
        # ccp.send_template_sms(mobile,[smses,5],1)

        send_sms.delay(mobile,smses)

        return res_json(errmsg='短信发送成功')



