import sqlite3
import json
import datetime

# 配置数据库文件
db_file = 'devicemanage.db'

# 数据库初始化
def create_database(db_file):
    conn = sqlite3.connect(db_file)
    c = conn.cursor()

    # 创建日志表
    c.execute('''CREATE TABLE IF NOT EXISTS log
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT DEFAULT (datetime('now', 'localtime')),
            message TEXT)''')

    # 创建证书表
    c.execute('''CREATE TABLE IF NOT EXISTS certificates
                (id INTEGER PRIMARY KEY AUTOINCREMENT,common_name TEXT, organization TEXT, organizational_unit TEXT,
                locality TEXT, state TEXT, country TEXT,
                issuer_common_name TEXT, issuer_organization TEXT, issuer_organizational_unit TEXT,
                issuer_locality TEXT, issuer_state TEXT, issuer_country TEXT,
                serial_number TEXT, valid_from TEXT, valid_until TEXT, certificate_file BLOB,
                added_time TEXT DEFAULT (datetime('now', 'localtime')))''')

    # 创建隧道表
    c.execute('''CREATE TABLE IF NOT EXISTS tunnel
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                tunnel_name TEXT, remote_server_ip TEXT, remote_server_port INTEGER, status TEXT,
                created_time TEXT DEFAULT (datetime('now', 'localtime')),
                certificate_id INTEGER, -- Add the certificate_id as a foreign key
                FOREIGN KEY (certificate_id) REFERENCES certificates(id))''')

    conn.commit()
    conn.close()

# 将时间字符串转换为 datetime 对象
def convert_to_datetime(time_string):
    time_format = '%Y%m%d%H%M%SZ'
    return datetime.datetime.strptime(time_string.decode(), time_format)


# 插入证书
def insert_certificate(certificate_data):
    conn = sqlite3.connect(db_file)
    c = conn.cursor()

    # 将日期时间对象转换为字符串
    certificate_data['valid_from'] = certificate_data['valid_from'].strftime('%Y-%m-%d %H:%M:%S')
    certificate_data['valid_until'] = certificate_data['valid_until'].strftime('%Y-%m-%d %H:%M:%S')
       # 插入证书数据
    c.execute('''INSERT INTO certificates
                (common_name, organization, organizational_unit,
                locality, state, country,
                issuer_common_name, issuer_organization, issuer_organizational_unit,
                issuer_locality, issuer_state, issuer_country,
                serial_number, valid_from, valid_until,certificate_file)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?)''',
              (certificate_data['common_name'], certificate_data['organization'], certificate_data['organizational_unit'],
               certificate_data['locality'], certificate_data['state'], certificate_data['country'],
               certificate_data['issuer_common_name'], certificate_data['issuer_organization'], certificate_data['issuer_organizational_unit'],
               certificate_data['issuer_locality'], certificate_data['issuer_state'], certificate_data['issuer_country'],
               certificate_data['serial_number'], certificate_data['valid_from'], certificate_data['valid_until'],
               certificate_data['certificate_file']))
    
    # 回传最后一次插入的证书ID
    certificate_id = c.lastrowid

    conn.commit()
    conn.close()

    return certificate_id

# 插入隧道
def insert_tunnel_data(tunnel_data):
    conn = sqlite3.connect(db_file)
    c = conn.cursor()

    c.execute('''INSERT INTO tunnel 
                 (tunnel_name, remote_server_ip, remote_server_port, status, certificate_id)
                 VALUES (?, ?, ?, ?, ?)''', 
              (tunnel_data['tunnel_name'], tunnel_data['remote_server_ip'], 
               tunnel_data['remote_server_port'], tunnel_data['status'], 
               tunnel_data['certificate_id']))

    conn.commit()
    conn.close()

# 插入日志
def insert_log(log_message):
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    
    c.execute("INSERT INTO log (message) VALUES (?)", (log_message,))

    conn.commit()
    conn.close()

# 下载证书文件
def read_certificate_file(certificate_id):
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    c.execute("SELECT certificate_file FROM certificates WHERE id=?", (certificate_id,))
    data = c.fetchone()
    if data:
        certificate_file_content = data[0]
        return certificate_file_content
    conn.close()
    return False

# 查询证书表
def query_certificates():
    conn = sqlite3.connect(db_file)
    c = conn.cursor()

    c.execute("SELECT * FROM certificates")
    rows = c.fetchall()

    # 构建结果字典列表
    result = []
    for row in rows:
        certificate_data = {
            'id':row[0],
            'common_name': row[1],
            'organization': row[2],
            'organizational_unit': row[3],
            'locality': row[4],
            'state': row[5],
            'country': row[6],
            'issuer_common_name': row[7],
            'issuer_organization': row[8],
            'issuer_organizational_unit': row[9],
            'issuer_locality': row[10],
            'issuer_state': row[11],
            'issuer_country': row[12],
            'serial_number': row[13],
            'valid_from': row[14],
            'valid_until': row[15],
            'added_time':row[17]
        }
        result.append(certificate_data)

    conn.close()

    # 转换为 JSON 格式
    json_result = json.dumps(result, indent=4)
    return json_result

# 查询隧道表
def query_tunnel():
    conn = sqlite3.connect(db_file)
    c = conn.cursor()

    c.execute('''SELECT * FROM tunnel''')
    rows = c.fetchall()
    result = []
    for row in rows:
        tunnel_data = {
            'id':row[0],
            'tunnel_name': row[1],
            'server_ip': row[2],
            'server_port': row[3],
            'status': row[4],
            'created_time': row[5],
            'cert_id': row[6],
        }
        result.append(tunnel_data)
    conn.close()
    json_result = json.dumps(result, indent=4)
    return json_result

def query_log():
    conn = sqlite3.connect(db_file)
    c = conn.cursor()

    c.execute('''SELECT * FROM log ORDER BY timestamp DESC''')
    rows = c.fetchall()
    result = []
    for row in rows:
        log_data = {
            'id':row[0],
            'timestamp': row[1],
            'logmessage': row[2]
        }
        result.append(log_data)
    conn.close()
    json_result = json.dumps(result, indent=4)
    return json_result