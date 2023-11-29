import sqlite3
import OpenSSL
import datetime
import json


def parse_certificate(pem_file_path):
    # 解析证书
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
        'valid_until': valid_until
    }

def convert_to_datetime(time_string):
    # 将时间字符串转换为 datetime 对象
    time_format = '%Y%m%d%H%M%SZ'
    return datetime.datetime.strptime(time_string.decode(), time_format)

def create_database(db_file):
    conn = sqlite3.connect(db_file)
    c = conn.cursor()

    # 创建证书表
    c.execute('''CREATE TABLE IF NOT EXISTS certificates
                (common_name TEXT, organization TEXT, organizational_unit TEXT,
                locality TEXT, state TEXT, country TEXT,
                issuer_common_name TEXT, issuer_organization TEXT, issuer_organizational_unit TEXT,
                issuer_locality TEXT, issuer_state TEXT, issuer_country TEXT,
                serial_number TEXT, valid_from TEXT, valid_until TEXT)''')

    conn.commit()
    conn.close()

def insert_certificate(db_file, certificate_data):
    # 插入证书解析结果
    conn = sqlite3.connect(db_file)
    c = conn.cursor()

    # 将日期时间对象转换为字符串
    certificate_data['valid_from'] = certificate_data['valid_from'].strftime('%Y-%m-%d %H:%M:%S')
    certificate_data['valid_until'] = certificate_data['valid_until'].strftime('%Y-%m-%d %H:%M:%S')
    # 插入证书数据
    c.execute('''INSERT INTO certificates
                VALUES (:common_name, :organization, :organizational_unit,
                :locality, :state, :country,
                :issuer_common_name, :issuer_organization, :issuer_organizational_unit,
                :issuer_locality, :issuer_state, :issuer_country,
                :serial_number, :valid_from, :valid_until)''', certificate_data)

    conn.commit()
    conn.close()

def query_certificates(db_file):
    # 查询证书表
    conn = sqlite3.connect(db_file)
    c = conn.cursor()

    c.execute("SELECT * FROM certificates")
    rows = c.fetchall()

    # 构建结果字典列表
    result = []
    for row in rows:
        certificate_data = {
            'common_name': row[0],
            'organization': row[1],
            'organizational_unit': row[2],
            'locality': row[3],
            'state': row[4],
            'country': row[5],
            'issuer_common_name': row[6],
            'issuer_organization': row[7],
            'issuer_organizational_unit': row[8],
            'issuer_locality': row[9],
            'issuer_state': row[10],
            'issuer_country': row[11],
            'serial_number': row[12],
            'valid_from': row[13],
            'valid_until': row[14]
        }
        result.append(certificate_data)

    conn.close()

    # 转换为 JSON 格式
    json_result = json.dumps(result, indent=4)
    return json_result


#test
pem_file_path = 'device1.pem'
db_file = 'devicemanage.db'

create_database(db_file)

certificate_data = parse_certificate(pem_file_path)

insert_certificate(db_file, certificate_data)

json_result = query_certificates(db_file)

print(json_result)
