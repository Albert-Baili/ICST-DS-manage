
import socket
import os

input_data=['1','device1.pem','exit']


BASE_DIR = os.path.dirname(os.path.abspath(__file__))  
PIC_DIR = os.path.join(BASE_DIR, 'certs')
pic_names = sorted(os.listdir(PIC_DIR))
pic_names = " ".join(i for i in pic_names)
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
try:
    mubiao_ip = '127.0.0.1'
    post = 7788

    addr = (mubiao_ip,int(post))
    s.connect(addr)
except IOError:
    print("您输入错误，请重新输入试！")
print("OK ! Connection is succefully...")
active = True
flag=0
while active:
    send_date = input("Press anter if you wangt to exit. And please input your message(1 cert or 2 word?): ")
    # send_date = input_data[flag]
    s.send(send_date.encode('utf-8'))
    print(send_date)
    if send_date=='exit' :
        s.close()
        break
    elif send_date == "1":
        data = input('cert?')
        cert_name = data 
        cert_path = os.path.join(PIC_DIR, cert_name) 
        file_size = os.stat(cert_path).st_size  
        file_info = '%s|%s' % (cert_name, file_size)  
        print("cert_path:{0},file_size:{1},file_info{2}".format(cert_path,file_size,file_info))
        s.sendall(bytes(file_info, 'utf-8'))
        print(cert_path)

        f = open(cert_path, 'rb') 
        has_sent = 0 
        while has_sent != file_size:  
            file = f.read(1024)  
            s.sendall(file)  
            has_sent += len(file)  
        f.close()  
        print('上传成功')
        print("wait...")
        BASE_DIR2 = os.path.dirname(os.path.abspath(__file__))

        data1 = s.recv(1024)
        filename, filesize = str(data1, 'utf8').split('|') 

        path = os.path.join(BASE_DIR2, filename) 
        filesize = int(filesize)
        ff = open(path, 'ab') 
        has_receive = 0  
      
        while has_receive != filesize:
            data1 = s.recv(1024)
            ff.write(data1) 
            has_receive += len(data1)  
        ff.close()  
        print('接受成功')
s.close()
