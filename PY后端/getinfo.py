import socket
def get_local_ip():
    try:
        # 创建一个socket对象
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # 连接到一个公共服务器（GoogleDNS服务器）
        s.connect(("8.8.8.8", 80))

        # 获取本地IP地址
        local_ip = s.getsockname()[0]

        # 关闭socket
        s.close()

        return local_ip
    except socket.error as e:
        return f"错误: {e}"

def scan_local_network():
    network_prefix = '192.168.0'  # 局域网的前缀是192.168.0.x
    active_devices = []

    for host in range(1, 255):
        ip_address = f"{network_prefix}.{host}"

        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.1)  # 设置连接超时时间

            # 尝试连接目标主机的7788端口
            result = s.connect_ex((ip_address, 7788))

            if result == 0:
                active_devices.append(ip_address)

            s.close()
        except socket.error:
            pass

    return active_devices

