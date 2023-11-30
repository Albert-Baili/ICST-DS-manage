# coding: utf-8
import io
import time
from flask import Flask,jsonify,request,send_file,render_template
from functools import wraps
import os

#设置用户登录Token
import jwt

#解决跨域问题
from flask_cors import CORS

#用户登录模块
from userLogin import login, info, logout, token_required

#主页模块
from getinfo import get_local_ip

#隧道测试模块
from tunnelTest import test_tunnel,tunnel_send_Info

#数据库模块
from sqlManage import create_database,read_certificate_file,query_certificates,query_log,query_tunnel,insert_log

#脱敏测试模块
from tuominTest.desensitizeYangai import handle_yangai_request
from tuominTest.desensitizeHash import handle_Hash_request

#配置数据库文件
db_file = 'devicemanage.db'

app = Flask(__name__)
CORS(app)  # 添加CORS中间件

@app.route('/')
def index():
    return render_template('index.html')


#用户登录与登出
@app.route('/vue-element-admin/user/login', methods=['POST'])
def login_route():
    log_message="用户登录"
    insert_log(log_message)
    return login()

@app.route('/vue-element-admin/user/info', methods=['get'])
@token_required
def info_route(token_payload):
    return info(token_payload)

@app.route('/vue-element-admin/user/logout', methods=['post'])
def logout_route():
    log_message="用户登出"
    insert_log(log_message)
    return logout()

#主页信息获取
@app.route('/api/dashbord/getIP',methods=['GET'])
def get_IP():
    LocalIP = get_local_ip()
    response = {
        'code': 20000,
        'data': LocalIP
    }
    log_message="获取本地IP地址"
    insert_log(log_message)
    return jsonify(response)

#隧道管理
@app.route('/api/test_tennel', methods=['GET'])
@token_required
def newtunnel(token_payload):
    target_ip = request.headers.get('targetip')
    target_port = int(request.headers.get('targetport'))
    tunnel_name=request.headers.get('tunnelname')
    certfile='device1.pem'#更新请求头
    log_message="用户尝试新建隧道，"+tunnel_name
    insert_log(log_message)
    return test_tunnel(tunnel_name,target_ip,target_port,certfile)

@app.route('/api/tunnel_manage/getalltunnels',methods=['GET'])
@token_required
def get_all_tunnels(token_payload):
    tunnels = query_tunnel()
    response = {
        'code': 20000,
        'data': tunnels
    }
    log_message="用户获取隧道列表信息"
    insert_log(log_message)
    return jsonify(response)


@app.route('/api/tunnel_manage/sendinfo',methods=['POST'])
@token_required
def tunnel_sendInfo(token_payload):
    log_message="用户进行隧道通信"
    insert_log(log_message)
    return tunnel_send_Info()

#证书管理
@app.route('/api/certificates/<int:certificate_id>', methods=['GET'])
def get_certificate_file(certificate_id):
    certificate_file_content = read_certificate_file(certificate_id)
    log_message="用户下载请求证书,证书ID:"+str(certificate_id)
    insert_log(log_message)
    if certificate_file_content:
        return send_file(
            io.BytesIO(certificate_file_content),
            as_attachment=True,
            attachment_filename=f'certificate_{certificate_id}.pem',
            mimetype='application/x-pem-file'
        )
    else:
        log_message="用户下载证书失败,请求的证书ID:"+str(certificate_id)
        insert_log(log_message)
        data={'message':'您查询的证书不存在'}
        response = {
            'code': 20000,
            'data': data
        }
        return jsonify(response)

@app.route('/api/certificates/getallcerts', methods=['GET'])
@token_required
def get_all_certs(token_payload):
    certs=query_certificates()
    response = {
        'code': 20000,
        'data': certs
    }
    log_message="用户获取证书列表信息"
    insert_log(log_message)
    return jsonify(response)

#日志管理
@app.route('/api/log_manage/getalllogs',methods=['GET'])
def get_all_logs():
    logs = query_log()
    response = {
        'code': 20000,
        'data': logs
    }
    return jsonify(response)

#脱敏测试
@app.route('/api/sendDesensiTest/yangai', methods=['POST'])
@token_required
def handle_yangai_tuomintest(token_payload):
    data = request.json
    response = handle_yangai_request(data)
    return jsonify(response)

@app.route('/api/sendDesensiTest/hash', methods=['POST'])
@token_required
def handle_hash_tuomintest(token_payload):
    data = request.json
    response = handle_Hash_request(data)
    return jsonify(response)

if __name__ == '__main__':
    create_database(db_file)
    app.debug = True
    app.run()
