from flask import Flask,jsonify,request

# 建立隧道
import socket
import os
import time

#解析证书
import OpenSSL

#导入数据库模块
from sqlManage import convert_to_datetime,insert_certificate,insert_tunnel_data

#配置信息
instrcutions=['1','exit']
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  
PIC_DIR = os.path.join(BASE_DIR, 'certs')
pic_names = sorted(os.listdir(PIC_DIR))
pic_names = " ".join(i for i in pic_names)

#数据库文件
db_file = 'devicemanage.db'

#建立隧道
def test_tunnel(tunnel_name,server_ip,sever_port,cert_file):
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
        mubiao_ip = server_ip
        post = sever_port
        addr = (mubiao_ip,int(post))
        s.connect(addr)
    except Exception as e:
        print("隧道连接失败！对方服务器不在线")
        data = {'message': f'隧道连接失败！发生异常：{e}'}
        response = {
            'code': 20000,
            'data': data
        }
        return jsonify(response)

    print("隧道建立成功，已连接对方服务器")
    active = True
    flag=0
    while active:
        try:
            send_date = instrcutions[flag]
            s.send(send_date.encode('utf-8'))

            time.sleep(1)
            print(send_date)
            if send_date=='exit' :
                print("接收到退出指令")
                s.close()
                break
            elif send_date == "1":
                print("接收到证书传输指令")
                cert_name = cert_file
                cert_path = os.path.join(PIC_DIR, cert_name) 
                file_size = os.path.getsize(cert_path)    
                file_info = '%s|%s' % (cert_name, file_size)  
                print("cert_path:{0},file_size:{1},file_info{2}".format(cert_path,file_size,file_info))
                s.sendall(bytes(file_info, 'utf-8'))
                print(cert_path)
                time.sleep(1)

                f = open(cert_path, 'rb') 
                has_sent = 0 
                while has_sent != file_size:  
                    file = f.read(1024)  
                    s.sendall(file)  
                    has_sent += len(file)  
                f.close()  
                print('客户端证书上传成功')
                print("wait...")
                
                time.sleep(1)
                BASE_DIR2 = os.path.dirname(os.path.abspath(__file__))
                data1 = s.recv(1024)
                filename, filesize = str(data1, 'utf8').split('|') 

                path = os.path.join(BASE_DIR2, filename)

                filesize = int(filesize)
                ff = open(path, 'wb') 
                has_receive = 0  
              
                while has_receive != filesize:
                    data1 = s.recv(1024)
                    ff.write(data1) 
                    has_receive += len(data1)  
                ff.close()  
                print('服务器证书接受成功')
            flag=flag+1
        except:
            data = {'message': '隧道测试失败！请重试或重启对方服务器'}
            response = {
                'code': 20000,
                'data': data
            }
            return jsonify(response)
    s.close()
    data = {'message': '隧道测试成功，双方已交换证书'}
    response = {
        'code': 20000,
        'data': data
    }
    #解析证书并存入数据库
    certificate_data = parse_certificate(path)
    latest_cert_id = insert_certificate(certificate_data)

    #保存隧道
    tunnel_data = {
        'tunnel_name': tunnel_name,
        'remote_server_ip': server_ip,
        'remote_server_port': sever_port,
        'status': 'Active',
        'certificate_id': latest_cert_id
    }
    insert_tunnel_data( tunnel_data)

    return jsonify(response)

# 解析证书
def parse_certificate(pem_file_path):
    print('解析证书ing')
    with open(pem_file_path, 'rb') as pem_file:
        pem_data = pem_file.read()

    certificate = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, pem_data)

    subject = certificate.get_subject()
    issuer = certificate.get_issuer()

    serial_number = '{:.0f}'.format(certificate.get_serial_number())  # 格式化序列号为不带小数位的字符串
    valid_from = convert_to_datetime(certificate.get_notBefore())
    valid_until = convert_to_datetime(certificate.get_notAfter())
    return {
        'common_name': subject.CN,
        'organization': subject.O,
        'organizational_unit': subject.OU,
        'locality': subject.L,
        'state': subject.ST,
        'country': subject.C,
        'issuer_common_name': issuer.CN,
        'issuer_organization': issuer.O,
        'issuer_organizational_unit': issuer.OU,
        'issuer_locality': issuer.L,
        'issuer_state': issuer.ST,
        'issuer_country': issuer.C,
        'serial_number': serial_number,
        'valid_from': valid_from,
        'valid_until': valid_until,
        'certificate_file':pem_data

    }

def tunnel_send_Info(server_ip,sever_port,send_data):
    data = request.get_json()
    server_ip=data['serverIP']
    sever_port=data['serverPort']
    send_data=data['sendData']
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
        addr = (server_ip,int(sever_port))
        s.connect(addr)
    except Exception as e:
        print("隧道连接失败！对方服务器不在线")
        response = {
            'code': 20000,
            'data': "隧道连接失败！对方服务器不在线"
        }
        return jsonify(response)
    
    print("隧道连接成功")
    try:
        send_instrcutions = '2'
        s.send(send_instrcutions.encode('utf-8'))
        time.sleep(1)
        # 发送十六进制数据
        s.send(send_data)
        s.close()
    except:
        print("信息发送有误")
        return

    response = {
            'code': 20000,
            'data': "消息发送"
        }
    return jsonify(response)