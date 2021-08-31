from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.auth.bce_credentials import BceCredentials
from baidubce.services.bos.bos_client import BosClient

## 设置BosClient的Host，Access Key ID和Secret Access Key
# bos_host = "http://bos.bj.baidubce.com"
# access_key_id = "aee47a29e8c345189b1f25f61590a724"
# secret_access_key = "b30e195099694c7bac90518924849bcc"
# # 创建BceClientConfiguration
# access=BceCredentials(access_key_id, secret_access_key)
# config = BceClientConfiguration(credentials=access, endpoint=bos_host)
# #新建BosClient
# bos_client = BosClient(config=config)
# #仓库名，上传后的文件名
# bucket_name='image01'
# key_name='1.jpg'
# #读取图片并上传
# with open('media/avatar.jpeg','rb') as f:
#     data=f.read()
#     res=bos_client.put_object_from_string(bucket=bucket_name, key=key_name,data=data)


#封装
class Img_cu(object):
    def __init__(self):
        self.bos_host = "bj.bcebos.com"
        self.access_key_id = "aee47a29e8c345189b1f25f61590a724"
        self.secret_access_key = "b30e195099694c7bac90518924849bcc"
    def up_img(self,fail):
        access = BceCredentials(self.access_key_id, self.secret_access_key)
        config = BceClientConfiguration(credentials=access, endpoint=self.bos_host)
        bos_client = BosClient(config=config)
        bucket_name = 'image01'
        key_name = '1234.jpg'
        try:
            res = bos_client.put_object_from_string(bucket=bucket_name, key=key_name, data=fail)
        except Exception as e:
            raise e
        else:
            res=res.__dict__
            if res['metadata']:
                print('图片上传成功')

with open('media/fluent_python_1.jpg','rb') as f:
     data=f.read()
     Img_cu().up_img(data)