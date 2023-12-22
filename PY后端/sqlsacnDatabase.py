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
            table_info TEXT
        )
    ''')
    conn.commit()
    conn.close()

def insert_data_into_table(json_data):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    for db_name, db_tables in json_data['databases'].items():
        # 将表信息转换为JSON字符串
        table_info_json = json.dumps(db_tables)
        cursor.execute('''
            INSERT INTO database_summary (
                database_version, database_type, database_name, table_info
            ) VALUES (?, ?, ?, ?)
        ''', (json_data['version'], json_data['type'], db_name, table_info_json))

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

    # 将每行的table_info从字符串转换为JSON对象
    data = [{
        "id": row[0],
        "database_version": row[1],
        "database_type": row[2],
        "database_name": row[3],
        "table_info": json.loads(row[4])  # 将字符串转换为JSON
    } for row in rows]

    response_data = {
        "result": data
    }
    response = {
        'code': 20000,
        'data': response_data
    }
    return response
