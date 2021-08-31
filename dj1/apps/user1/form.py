from django import forms
from .models import User
from django.db.models import Q
from django.contrib.auth import login
from user1 import constants
class Loginform(forms.Form):
    user_account=forms.CharField()
    password=forms.CharField(max_length=18,min_length=6,
                             error_messages={'max_length':'密码长度需小于18',
                                             'min_length':'密码长度需大于6',
                                             'required':'密码不能为空'})
    status=forms.BooleanField(required=False)
    #重写request，设置session
    def __init__(self,*args,**kwargs):
        self.request=kwargs.pop('request')
        super().__init__(*args,**kwargs)
    #效验用户名
    def clean_user_account(self):
        user_info=self.cleaned_data.get('user_account')
        if not user_info:
            raise forms.ValidationError('手号码或用户名不能为空')
        if len(user_info)<3 or len(user_info)>11:
            raise forms.ValidationError('手号码或用户名格式错误')
        return user_info
    def clean(self):
        bs=super().clean()
        user_account=bs.get('user_account')
        password=bs.get('password')
        status=bs.get('status')
        user_check=User.objects.filter(Q(mobile=user_account)|Q(username=user_account))
        if user_check:
            user=user_check.first()
            if user.check_password(password): #django自带方法验证密码
                if status:
                    self.request.session.set_expiry(constants.USER_SESSION_EXPIRES) #设置session
                else:
                    self.request.session.set_expiry(constants.SESSION_TIME)
                login(self.request,user)
            else:
                raise forms.ValidationError('用户名或密码错误')
        else:
            raise forms.ValidationError('此用户不存在')