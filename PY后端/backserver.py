# coding: utf-8
import io
import time
from flask import Flask,jsonify,request,send_file,render_template,send_from_directory
from functools import wraps
import os

#设置用户登录Token
import jwt

#解决跨域问题
from flask_cors import CORS

##大屏模块
#脱敏信息
from datamark import dealwithcsv,tuominLists

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
from tuominTest.desensitizeJiami import des_encrypt_api,aes_encrypt_api
from tuominTest.desensitizeSM4 import sm4_encrypt_api


#数据库扫描模块
from sqlsacnDatabase import get_database_summary

#配置数据库文件 sqlite
db_file = 'devicemanage.db'

app = Flask(__name__,static_folder='dist-dashboard/static', static_url_path='/static')
CORS(app)  # 添加CORS中间件

@app.route('/manage/<path:path>')
def serve_app1(path):
    if path != "" and os.path.exists("dist-manage/" + path):
        return send_from_directory('dist-manage', path)
    else:
        return send_from_directory('dist-manage', 'index.html')

@app.route('/dashboard/<path:path>')
def serve_app2(path):
    if path != "" and os.path.exists("dist-dashboard/" + path):
        return send_from_directory('dist-dashboard', path)
    else:
        return send_from_directory('dist-dashboard', 'index.html')

@app.route('/')
def index():
    # 访问根URL时加载哪个应用
    return send_from_directory('dist-dashboard', 'index.html')

#大屏模块
@app.route('/gettuolinLists', methods=['GET'])
def gettuolinLists():
 return {
    'success':True,
    'data':{
       'list':tuominLists[-40:]
    }
 }

@app.route('/api/asset_num', methods=['GET', 'POST'])
def get_data():
    msg = {'success': True,
           'data': {'alarmNum': 2, 'offlineNum': 17, 'onlineNum': 22, 'totalNum': 39},
           'msg': '出错啦！'}
    return jsonify(msg)


@app.route('/api/asset_info', methods=['GET', 'POST'])
def get_info():
    info = {
        'success': True,
        'data':
            [
                {
                    'devicename': 'Personal Computer',
                    'onlineState': 1,
                    'IP': '192.168.123.46',
                    'mac': '04:7C:16:DC:7A:D6'

                },
                {
                    'devicename': 'CyberTAN Technology',
                    'onlineState': 1,
                    'IP': '192.168.123.198',
                    'mac': '28:39:26:63:39:9D'

                },
                {
                    'devicename': 'Micro-Star Intl',
                    'onlineState': 1,
                    'IP': '192.168.123.45',
                    'mac': '24:7C:26:DC:7A:A6'

                },
                {
                    'devicename': 'Beijing Xiaomi Mobile Software',
                    'onlineState': 1,
                    'IP': '192.168.123.1',
                    'mac': 'D4:DA:21:0B:89:4F'

                },
                {
                    'devicename': 'Ruijie Networks',
                    'onlineState': 1,
                    'IP': '10.133.24.1',
                    'mac': '58:69:6C:4C:47:53'

                },
            ],
        'msg': '出错啦！',
    }
    return jsonify(info)

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
            download_name=f'certificate_{certificate_id}.pem',
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
def get_all_certs():
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

@app.route('/api/sendDesensiTest/des',methods=['POST'])
def handle_jiami_tuomintest():
    data = request.json
    enc_rule = data.get('encRule')
    if enc_rule == '1':
        # 调用SM4加密函数
         response =sm4_encrypt_api(data)
    elif enc_rule == '2':
        # 调用DES加密函数
        response = des_encrypt_api(data)
    elif enc_rule == '3':
        # 调用DES加密函数
        response = aes_encrypt_api(data)
    else:
        # 未知的加密规则
        response= {
            'code': 20000,
            'data': {'result': 'Error, unknown encryption rule.'}
        }
    return jsonify(response)

#数据库扫描
@app.route('/api/sql_scan/get_sql_data', methods=['GET'])
def get_sqldDB_data():
    response = get_database_summary()
    return jsonify(response)

if __name__ == '__main__':
    create_database(db_file)
    app.debug = True
    app.run()
