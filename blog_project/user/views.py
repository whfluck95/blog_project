import jwt
import time
import json
import hashlib
from django.http import JsonResponse
from django.shortcuts import render
from .models import *


# Create your views here.
def users(request):
    if request.method == 'GET':
        # 获取用户数据
        return JsonResponse({'code': 200})

    elif request.method == 'POST':
        # 创建用户
        # 前端注册页面地址 http://127.0.0.1:5000/register
        json_str = request.body
        if not json_str:
            result = {'code': 201, 'error': 'Please give me data'}
            return JsonResponse(request)
        json_obj = json.loads(json_str)

        username = json_obj.get('username')
        if not username:
            result = {'code': 202, 'error': 'Please give me username'}
            return JsonResponse(request)
        email = json_obj.get('email')
        if not email:
            result = {'code': 202, 'error': 'Please give me email'}
            return JsonResponse(result)
        password1 = json_obj.get('password_1')
        password2 = json_obj.get('password_2')
        if not password1 or not password2:
            result = {'code': 204, 'error': 'Please give me password'}
        if password1 != password2:
            result = {'code': 205, 'error': 'Your password not same'}
            return JsonResponse(result)
        # 优先查询当前用户名是否已经存在
        old_user = UserProfile.objects.filter(username=username)
        if old_user:
            result = {'code': 206, 'error': 'Your username is already existed'}
            return JsonResponse(result)
        # 密码处理md5哈希/散列
        m = hashlib.md5()
        m.update(password1.encode())
        sign = info = ''
        try:
            UserProfile.objects.create(
                username=username,
                nickname=username,
                email=email,
                password=m.hexdigest(),
                sign=sign,
                info=info,
            )
        except Exception as e:
            #数据库down 用户名已存在
            result = {'code':207,'error':'Server is busy'}
            return JsonResponse(result)
        #make token
        token = make_token(username)

        #正常返回给前端
        result = {'code':200,'username':username,'data':{'token':token.decode()}}

    elif request.method == 'PUT':
        # 更新数据
        pass
    else:
        raise

    return JsonResponse({'code': 200})



def make_token(username,expire=3600*24):
    """定义token函数"""
    key = '123456'
    now = time.time()
    payload = {'username':username,'exp':int(now+expire)}
    return jwt.encode(payload,key,algorithm='HS256')
