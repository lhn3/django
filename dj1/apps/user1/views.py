from django.shortcuts import render,HttpResponse,redirect,reverse
from django.views.generic import View
import json,re
from dj1.response_code import res_json,Code
from user1.models import User
from django_redis import get_redis_connection
from django.contrib.auth import login,logout
from .form import Loginform
# Create your views here.

#注册
class Register(View):
    def get(self,request):
        return render(request,'users/register.html')
    def post(self,request):
        Data = request.body
        Data = json.loads(Data)
        username = Data.get('username')
        password = Data.get('password')
        password_re = Data.get('password_re')
        mobile = Data.get('mobile')
        sms_code = Data.get('sms_code')

        #判断传入后端数据是否都存在
        if not all([username,password_re,password,mobile,sms_code]):
            return res_json(errno=Code.NODATA,errmsg='数据不完整，请重新输入')

        #判断用户名时候合规或是否存在
        if not re.match('^[\u4e00-\u9fa5\w]{3,10}$',username):
            return res_json(errno=Code.DATAERR,errmsg='用户名格式错误1')
        if User.objects.filter(username=username).count():
            return res_json(errno=Code.DATAEXIST,errmsg='用户名已存在')

        #判断密码是否存在、合规、两次密码是否相同
        if not re.match('^[0-9a-zA-Z]{6,18}$',password):
            return res_json(errno=Code.DATAERR,errmsg='密码输入不规范')
        if password_re != password:
            return res_json(errno=Code.DATAERR,errmsg='两次密码输入不一致')

        #判断手机号是否合规，是否存在
        if not re.match('^1[3-9]\d{9}$',mobile):
            return res_json(errno=Code.DATAERR,errmsg='号码格式不正确')
        if User.objects.filter(mobile=mobile).count():
            return res_json(errno=Code.DATAEXIST,errmsg='此号码已被注册')

        #判断短信验证码
        connent_redis=get_redis_connection('verify')
        smses=connent_redis.get('sms_{}'.format(mobile))
        smses=smses.decode()
        if smses is None:
            return res_json(errno=Code.NODATA,errmsg='短信验证码已过期')
        if sms_code != smses:
            return res_json(errno=Code.DATAERR,errmsg='短信验证码错误')
        #取出即删除
        try:
            connent_redis.delete('sms_{}'.format(mobile))
            connent_redis.delete('smsflag_{}'.format(mobile))
        except:
            pass

        #注册
        user=User.objects.create_user(
            username=username,
            password=password,
            mobile=mobile,
        )
        #立即登录，并保存14天session
        login(request,user)

        return res_json(errmsg='注册成功！')

#登录
class Login(View):
    def get(self,request):
        return render(request, 'users/login.html')
    def post(self,request):
        data=request.body
        if not data:
            return res_json(errno=Code.NODATA,errmsg='输入数据无效，请重新输入')
        data=json.loads(data)
        #向表单传入数据
        form=Loginform(data=data,request=request)
        # 表单验证成功处理
        if form.is_valid():   #返回布尔值，验证成功返回True
            return res_json(errmsg='登陆成功')
        #验证失败处理
        else:
            mlist=[]
            for i in form.errors.get_json_data().values():  #遍历表单中的报错
                mlist.append(i[0].get('message'))           #索引获取报错内容并添加在列表中
                msg='/'.join(mlist)
                return res_json(errno=Code.LOGINERR,errmsg=msg)

#退出
class Logout(View):
    def get(self,request):
        logout(request)
        return redirect(reverse('login'))

#找回密码
class Find_pwd(View):
    def get(self,request):
        return render(request,'users/find_pwd.html')
    def post(self,request):
        Data = request.body
        Data = json.loads(Data)
        password = Data.get('password')
        mobile = Data.get('mobile')
        sms_code = Data.get('sms_code')

        # 判断传入后端数据是否都存在
        if not all([password, mobile, sms_code]):
            return res_json(errno=Code.NODATA, errmsg='数据不完整，请重新输入')

        # 判断密码是否存在、合规
        if not re.match('^[0-9a-zA-Z]{6,18}$', password):
            return res_json(errno=Code.DATAERR, errmsg='新密码输入不规范')

        # 判断手机号是否合规，是否存在
        if not re.match('^1[3-9]\d{9}$', mobile):
            return res_json(errno=Code.DATAERR, errmsg='号码格式不正确')
        user=User.objects.get(mobile=mobile)
        if not user:
            return res_json(errno=Code.DATAEXIST, errmsg='此号码没有被注册')

        # 判断短信验证码
        connent_redis = get_redis_connection('verify')
        smses = connent_redis.get('sms_{}'.format(mobile))
        smses = smses.decode()
        if smses is None:
            return res_json(errno=Code.NODATA, errmsg='短信验证码已过期')
        if sms_code != smses:
            return res_json(errno=Code.DATAERR, errmsg='短信验证码错误')
        # 取出即删除
        try:
            connent_redis.delete('sms_{}'.format(mobile))
            connent_redis.delete('smsflag_{}'.format(mobile))
        except:
            pass
        # 修改密码
        user.set_password(password)
        user.save()
        return res_json(errmsg='密码找回成功！')

#修改密码
class Re_pwd(View):
    def get(self,request):
        return render(request,'users/re_pwd.html')
    def post(self,request):
        data=request.body
        data=json.loads(data)
        old=data.get('old')
        new=data.get('new')
        username=request.user
        if not all([old,new,username]):
            return res_json(errno=Code.DATAERR,errmsg='信息不完整')
        user=User.objects.get(username=username)
        if not user.check_password(old):
            return res_json(errno=Code.PWDERR,errmsg='旧密码输入有误')
        if not 6 <= len(new) <= 18:
            return res_json(errno=Code.DATAERR,errmsg='新密码格式错误')
        if old==new:
            return res_json(errno=Code.DATAERR,errmsg='新密码不能与旧密码相同')
        user.set_password(new)
        user.save()
        return res_json(errmsg='密码修改成功')




