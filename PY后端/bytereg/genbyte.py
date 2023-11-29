import random

def generate_random_message():
    # 生成随机的协议ID和有效数据长度
    protocol_id = random.randint(0, 255)
    data_length = random.randint(1, 20)  # 有效数据长度范围为1到20字节

    # 生成随机的有效数据部分
    data = [random.randint(0, 255) for _ in range(data_length)]

    # 计算校验值
    checksum = sum(data) & 0xFF

    # 构建报文
    message = [0xac, 0xbc, protocol_id, data_length] + data + [checksum, 0xfc]
    return bytes(message)

# 测试生成报文
if __name__ == "__main__":
    random_message = generate_random_message()
    print("随机生成的报文：", random_message.hex())
