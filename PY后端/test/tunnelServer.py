import socket
import os
import time

def parse_message(data):
    # 遍历数据查找帧头0xacbc
    start_index = -1
    for i in range(len(data) - 1):
        if data[i] == 0xac and data[i + 1] == 0xbc:
            start_index = i
            print("检测到帧头")
            break

    if start_index == -1:
        print("没有检测到帧头")
        return None, data  # 没有找到帧头

    # 检查数据长度是否足够
    if start_index + 4 >= len(data):
        print("数据长度不足1")
        return None, data[start_index:]  # 数据长度不足

    # 提取协议ID和有效数据长度
    protocol_id = data[start_index + 2]
    print("协议ID"+str(protocol_id))
    data_length = data[start_index + 3]
    print("数据长度"+str(data_length))

    # 检查剩余数据长度是否足够
    if start_index + 4 + data_length + 2 > len(data):
        print("数据长度不足2")
        return None, data[start_index:]  # 数据长度不足

    # 提取数据部分和校验值
    payload = data[start_index + 4: start_index + 4 + data_length]
    checksum = data[start_index + 4 + data_length]

    # 验证校验值
    calculated_checksum = sum(payload) & 0xFF
    if checksum != calculated_checksum:
        print("校验失败")
        return None, data[start_index + 1:]  # 校验失败

    # 检查帧尾0xfc
    if data[start_index + 4 + data_length + 1] != 0xfc:
        return None, data[start_index + 2:]  # 帧尾错误

    print("检测到帧尾")

    # 提取完整消息
    message = data[start_index+4: start_index + 4 + data_length]

    # 返回提取的消息和未识别部分的数据
    return message, data[start_index + 4 + data_length + 2:]

def main():
    # 1,create
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 2,bind
    s.bind(("", 7788))
    # 3,listen
    s.listen(128)
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))  
    PIC_DIR = os.path.join(BASE_DIR, 'certs')  
    pic_names = sorted(os.listdir(PIC_DIR))  

    pic_names = " ".join(i for i in pic_names) 


    while True:
        print ("wait the new session... ")
        # 4,accept
        new_s, client_addr = s.accept() #等待客户端的连接，并创建一个新的套接字，给客户端服务
        flag=0
        while True:
            flag=flag+1
            print("正在连接... ", client_addr[0])
            resv_date = new_s.recv(1024) #接受客户端发来的请求
            # print(resv_date)
            print("com from {0} the news: ".format(client_addr[0]),resv_date)
            if flag>5:
                break
            if resv_date.decode('utf-8') == "2":
                print("接收到接收信息指令")
                data = new_s.recv(1024)
                parse_message(data)
                print(data)
                break
            if resv_date.decode('utf-8') == "exit":
                print("接收到退出指令")
                break
            if resv_date.decode('utf-8') == "1":
                print("接收到证书传输指令准备开始传输")
                data = new_s.recv(1024)
                print(data)
                filename, filesize = str(data, 'utf8').split('|')  
                path = os.path.join(BASE_DIR, filename)  
                filesize = int(filesize)  
                print(path)
                f = open(path, 'wb')  
                has_receive = 0  
                while has_receive != filesize:
                    data1 = new_s.recv(1024) 
                    f.write(data1)  # 写入
                    print('正在写入')
                    print(data1)
                    has_receive += len(data1)  
                f.close()
                print('客户端证书接受成功')

                time.sleep(1)
                cert1 = 'device2.pem'
                cert_path = os.path.join(PIC_DIR, cert1)  
                file_size = os.path.getsize(cert_path)
                file_info2 = '%s|%s' % (cert1, file_size)  
                new_s.send(bytes(file_info2, 'utf-8'))
               
                time.sleep(1)
                ff = open(cert_path, 'rb')  
                has_sent = 0  
                while has_sent != file_size:  
                    file = ff.read(1024) 
                    new_s.sendall(file)  
                    has_sent += len(file) 
                ff.close()  
                
                print('服务器证书发送成功')
                
        new_s.close()
        print("over----")

    # 5,close
    s.close()


if __name__ == '__main__':
    main()


