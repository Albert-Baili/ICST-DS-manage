import csv
import re
from datetime import datetime

tuominLists=[]

# 数据掩盖函数
def mask_sensitive_data(data):
    # 使用正则表达式来查找和替换用户名和电子邮件
    username_pattern = re.compile(r'\b\w+\b')
    email_pattern = re.compile(r'\b[\w.-]+@[a-zA-Z]+\.[a-zA-Z]+\b')
    
    # 替换用户名和电子邮件地址为虚拟值
    masked_data = username_pattern.sub('***MASKED***', data)
    masked_data = email_pattern.sub('***MASKED***', masked_data)
    return masked_data

# 范围模糊化函数
def precise_range_mask_age_data(age):
    age_ranges_mapping = {
        (0, 10): "0-10岁",
        (11, 20): "11-20岁",
        (21, 30): "21-30岁",
        (31, 40): "31-40岁",
        (41, 50): "41-50岁",
        (51, 60): "51-60岁",
        (61, 70): "61-70岁",
        (71, 80): "71-80岁",
        (81, 90): "81-90岁",
        (91, float('inf')): "91岁以上"
    }
    # 替换年龄字段为范围值
    for age_range, age_range_label in age_ranges_mapping.items():
        if age_range[0] <= int(age) <= age_range[1]:
            age = age_range_label
            break
    return age

def precise_range_mask_balance_data(balance): 
    balance_ranges_mapping = {
        (0, 1000): "0-1000",
        (1001, 5000): "1001-5000",
        (5001, 10000): "5001-10000",
        (10001, 20000): "10001-20000",
        (20001, float('inf')): "20001~"
    }
    
    for balance_range, balance_range_label in balance_ranges_mapping.items():
        if balance_range[0] <= float(balance) <= balance_range[1]:
            balance = balance_range_label
            break
    return balance

# 构建字段名与脱敏方法的映射字典
desensitize_functions = {
    'Username': mask_sensitive_data,
    'Email': mask_sensitive_data,
    'Age': precise_range_mask_age_data,
    'Balance': precise_range_mask_balance_data,
}

# 构建字段名与脱敏方法的映射字典
sensitive_chengdu = {
    'Username': '高',
    'Email': '中',
    'Age': '中',
    'Balance': '低',
}

def dealwithcsv(suggestions,file_id):
    with open('uploads/'+str(file_id)+'.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        # 输出CSV文件的表头
        # print("表头:", reader.fieldnames)
        # print("脱敏建议:", suggestions)
        for row in reader:
            for field, suggestion in suggestions.items():
                if field in row and field in desensitize_functions:
                    # 根据建议对字段进行脱敏
                    row[field] = desensitize_functions[field](row[field])
                    log_record = {
                        'ziduan': field,
                        'minganchengdu':sensitive_chengdu[field],
                        'tuominmethod': suggestion,
                        'source':file_id[:8],
                        'time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        'aftertuomin': row[field],
                    }
                    tuominLists.append(log_record)
            # 处理完毕后，输出脱敏后的行数据
            # print(row)
        return {'success': 'ok'}

suggestions = {'Age': 'range', 'Balance': 'range', 'Email': 'mask', 'User ID': 'none', 'Username': 'mask'}
file_id = '6ca37548cd36d1eeb91bc00f8a55ade8e0a5e75f2399b76fd239445fe3abad62'
dealwithcsv(suggestions, file_id)

