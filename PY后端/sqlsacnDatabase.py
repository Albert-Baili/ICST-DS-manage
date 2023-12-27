import sqlite3
import json

db_file='mysql_scan.db'

def create_db_table():
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS database_summary (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            database_version TEXT,
            database_type TEXT,
            database_name TEXT,
            grants_info TEXT,
            database_size REAL,
            table_info TEXT
        )
    ''')
    conn.commit()
    conn.close()

def insert_data_into_table(json_data):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    grants_info_json = json.dumps(json_data['grants'])


    for db_name, db_content in json_data['databases'].items():
        table_info_json = json.dumps(db_content.get('table', {}))
        db_size = db_content.get('size')
        cursor.execute('''
            INSERT INTO database_summary (
                database_version, database_type, database_name, grants_info, database_size, table_info
            ) VALUES (?, ?, ?, ?, ?, ?)
        ''', (json_data['version'], json_data['type'], db_name, grants_info_json, db_size, table_info_json))

    conn.commit()
    conn.close()

def read_json_file(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def main():
    create_db_table()
    json_data = read_json_file('database_info.json')
    insert_data_into_table(json_data)
    print("Data insertion complete.")

def get_database_summary():
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM database_summary')
    rows = cursor.fetchall()
    conn.close()

    # 将每行的数据转换为字典，并处理JSON字段
    data = [{
        "id": row[0],
        "database_version": row[1],
        "database_type": row[2],
        "database_name": row[3],
        "grants_info": json.loads(row[4]),  # 将字符串转换为JSON
        "database_size": row[5],
        "table_info": json.loads(row[6])   # 将字符串转换为JSON
    } for row in rows]

    response_data = {
        "result": data
    }
    response = {
        'code': 20000,
        'data': response_data
    }
    return response