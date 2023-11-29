import socket

def start_client(server_ip, server_port):
    # 创建客户端 socket 对象
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 连接服务器
    client_socket.connect((server_ip, server_port))
    print("与服务器建立连接")

    # 发送 device1.pem 文件给服务器
    with open('device1.pem', 'rb') as f:
        while True:
            data1 = f.read(4096)
            print(data1)
            if not data1:
                break
            client_socket.sendall(data1)
    print("发送 device1.pem 文件")

    # 发送文件传输完成标志
    client_socket.sendall(b'FILE_TRANSFER_COMPLETE')
    

    # # 接收服务器发送的 device2.pem 文件
    # with open('recived_device2.pem', 'wb') as f:
    #     while True:
    #         data2 = client_socket.recv(4096)
    #         if not data2:
    #             break
    #         f.write(data2)
    # print("接收到 device2.pem 文件")

    # 关闭连接
    client_socket.shutdown(socket.SHUT_RDWR)
    client_socket.close()
    print("与服务器的连接已关闭")

# 运行客户端
start_client('localhost', 12345)

# def verify_callback(connection, cert, errnum, depth, ok):
#     # 自定义验证逻辑
#     if depth == 0 and cert.subject.CN == 'localhost':
#         return True
#     return False

# def start_client(serverip,serverport):
#     # 创建socket对象
#     client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
#     # 创建SSL上下文
#     ssl_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
#     ssl_context.load_cert_chain(certfile='device1.pem', keyfile='prikey.pem')
     
#     ssl_context.check_hostname = False
#     ssl_context.verify_mode = ssl.CERT_NONE
    
#     ssl_context.verify_callback = verify_callback
      
#     # SSL握手
#     ssl_socket = ssl_context.wrap_socket(client_socket, server_hostname=serverip)
    
#     # 连接服务器
#     ssl_socket.connect((serverip, serverport))
#     print("与服务器建立连接")
    
#     # 发送客户端证书
#     with open('client.crt', 'rb') as f:
#         client_cert = f.read()
#     ssl_socket.sendall(client_cert)
#     print("发送客户端证书")
    
#     # 接收服务器证书
#     server_cert = ssl_socket.recv(4096)
#     with open('server.crt', 'wb') as f:
#         f.write(server_cert)
#     print("接收到服务器证书")
    
#     # 关闭连接
#     ssl_socket.shutdown(socket.SHUT_RDWR)
#     ssl_socket.close()
#     print("与服务器的连接已关闭")