from flask import Flask,jsonify,request
from datetime import datetime, timedelta 
from functools import wraps

#设置用户登录Token
import jwt

# 用于存储用户信息
users = {
    'admin': '123456',
    'editor':'654321'
}

# 生成 Token 的函数
def generate_token(username):
    payload = {
        'username': username,
        'exp': datetime.utcnow() + timedelta(minutes=20)  # 设置有效期为20分钟
    }
    token = jwt.encode(payload, 'secret_key', algorithm='HS256')
    return token

# 验证 Token 的装饰器
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Token')
        print(token)
        if token:
            try:
                payload = jwt.decode(token, 'secret_key', algorithms=['HS256'])
                if datetime.utcnow() <= datetime.fromtimestamp(payload['exp']):
                    return f(*args,token_payload=payload, **kwargs)
            except jwt.ExpiredSignatureError:
                pass
        else:
            data={'message':'非法访问'}
            response = {
                'code': 50008,
                'data': data
            }

        data={'message':'会话已经过期'}
        response = {
            'code': 50008,
            'data': data
        }
        return jsonify(response)

    return decorated

def login():
    data = request.get_json()
    username=data['username']
    password=data['password']
    if username and password and users.get(username) == password:
        token = generate_token(data['username'])
        data={"token":token}
        response = {
            'code': 20000,
            'data': data
        }
        # response.headers.add('Access-Control-Allow-Origin', '*')  # 允许所有域的请求
        return jsonify(response)
    else:
        data={'message':'登录失败，请检查用户名与密码'}
        response = {
            'code': 60204,
            'data': data
        }
        return jsonify(response)

def info(token_payload):
    if token_payload['username'] == 'admin':
        user_info = {
            'roles': ['admin'],
            'introduction': 'I am a super administrator',
            'avatar': 'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif',
            'name': 'super Admin'
        }
    if token_payload['username'] == 'editor':
        user_info={
            'roles': ['editor'],
            'introduction': 'I am an editor',
            'avatar': 'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif',
            'name': 'Normal Editor'
        }
    response = {
        'code': 20000,
        'data': user_info
    }
    return jsonify(response)

def logout():
    response = {
        'code': 20000,
        'data': "success"
    }
    return jsonify(response)