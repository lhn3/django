from django import template
from datetime import datetime
register=template.Library()
import pytz
@register.filter
def foxes(data):
    now=datetime.now() #不含时区
    now=now.replace(tzinfo=pytz.timezone('UTC'))
    bs=(now-data).total_seconds()
    if bs<60:
        return '刚刚'
    elif 60<=bs<60*60:
        min=int(bs//60)
        return '{}分钟前'.format(min)
    elif 60*60<=bs<60*60*24:
        hours=int(bs//(60*60))
        return '{}小时前'.format(hours)
    elif 60*60*24<=bs<60*60*24*30:
        day=int(bs//(60*60*24))
        return '{}天前'.format(day)
    elif 60*60*24*30<=bs<60*60*24*7*52:
        month=int(bs//(60*60*24*30))
        return '{}月前'.format(month)
    elif 60*60*24*7*52<=bs<=60*60*24*7*52*3:
        year=int(bs//(60*60*24*7*52))
        return '{}年前'.format(year)
    elif 60*60*24*7*52*3<bs:
        return data.replace(tzinfo=pytz.timezone('Asia/Shanghai'))