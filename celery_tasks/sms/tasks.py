from yuntongxun.sms import CCP
from celery_tasks.main import celery_app
import logging
logger=logging.getLogger('django')

@celery_app.task(bind=True,name='send_sms',retry_backoff=3)
def send_sms(self,mobile,smses):
    try:
        res=CCP().send_template_sms(mobile,[smses,5],1)
    except Exception as e:
        logger.error(e)
        raise self.retry(exc=e,max_retries=3)
    if res !=0:
        raise self.retry(exc=Exception('短信发送失败'),max_retries=3)
    return res