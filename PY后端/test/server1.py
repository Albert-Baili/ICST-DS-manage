import socket

def start_server(server_ip, server_port):
    # 创建服务器 socket 对象
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_ip, server_port))
    server_socket.listen(1)
    print("等待客户端连接...")

    # 接受客户端连接
    client_socket, client_address = server_socket.accept()
    print("与客户端建立连接：", client_address)

    # 接收客户端发送的 device1.pem 文件
    with open('recived_device1.pem', 'wb') as f:
        while True:
            data1 = client_socket.recv(4096)
            if not data1:
                break
            f.write(data1)
    print("接收到 device1.pem 文件")

    # # 发送 device2.pem 文件给客户端
    # with open('device2.pem', 'rb') as f:
    #     while True:
    #         data2 = f.read(4096)
    #         if not data2:
    #             break
    #         client_socket.sendall(data2)
    # print("发送 device2.pem 文件")

    # # 发送文件传输完成标志
    # client_socket.sendall(b'FILE_TRANSFER_COMPLETE')

    # 关闭连接
    client_socket.shutdown(socket.SHUT_RDWR)
    client_socket.close()
    server_socket.close()
    print("与客户端的连接已关闭")

# 运行服务器
start_server('localhost', 12345)
