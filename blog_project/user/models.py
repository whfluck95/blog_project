from django.db import models

# Create your models here.

#class -> UserProfile
#表名 user_profile
#username, nickname,email,password,sign,info,avatar

class UserProfile(models.Model):

    username = models.CharField(max_length=11,verbose_name='用户名',primary_key=True)
    nickname = models.CharField(max_length=30,verbose_name='昵称')
    email = models.CharField(max_length=50,verbose_name='邮箱',null=True)
    password = models.CharField(max_length=32,verbose_name='密码')
    sign = models.CharField(max_length=50,verbose_name='个人签名')
    info = models.CharField(max_length=150,verbose_name='个人描述')
    avatar = models.ImageField(upload_to='avatar/')
    created_time = models.DateField(verbose_name='创建时间')
    updated_time = models.DateField(verbose_name='更新时间')

    class Meta:
        db_table = 'user_profile'