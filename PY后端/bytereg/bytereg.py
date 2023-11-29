# 建立隧道
import socket
import os
import time

import random

def generate_random_message():
    # 生成随机的协议ID和有效数据长度
    protocol_id = random.randint(1, 3)
    data_length = random.randint(1, 10) # 有效数据长度范围为1到10字节

    # 生成随机的有效数据部分
    data = [random.randint(0, 255) for _ in range(data_length)]
    print(data)

    # 计算校验值
    checksum = sum(data) & 0xFF

    # 构建报文
    message = message = bytes([0xac, 0xbc, protocol_id, data_length]) + bytes(data) + bytes([checksum, 0xfc])
    return message


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

    if protocol_id == 3:
        print("该条消息为密文消息")
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

def tunnel_connect(server_ip,sever_port,send_data):
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
        addr = (server_ip,int(sever_port))
        s.connect(addr)
    except Exception as e:
        print("隧道连接失败！对方服务器不在线")
        return
    
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

    print("隧道建立成功，已连接对方服务器")

# 测试
if __name__ == "__main__":
    raw_data = generate_random_message()
    print(raw_data)
    remaining_data = raw_data

    tunnel_connect("127.0.0.1",7788,raw_data)
    message, remaining_data = parse_message(remaining_data)
    if message:
        print("识别到消息：", message.hex())
    else:
        print("未能识别完整消息，剩余数据：", remaining_data.hex())