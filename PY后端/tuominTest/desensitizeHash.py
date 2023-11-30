import hashlib
from gmssl import sm3, func

def handle_Hash_request(data):
    print(data)
    name = data.get('name')
    origindata = data.get('origindata')
    hashRule = int(data.get('hashRule', 0))

    if hashRule == 1:
        # 使用 SHA256 进行哈希
        hashed_data = hashlib.sha256(origindata.encode()).hexdigest()
    elif hashRule == 2:
        # 使用 SHA512 进行哈希
        hashed_data = hashlib.sha512(origindata.encode()).hexdigest()
    elif hashRule == 3:
        # 使用 SM3 进行哈希
        hashed_data = sm3.sm3_hash(func.bytes_to_list(origindata.encode()))
    else:
        # 未定义的 hashRule
        hashed_data = "未定义的哈希规则"

    response_data = {
        "result":  hashed_data
    }
    response = {
        'code': 20000,
        'data': response_data
    }
    return response
