def yangai_rule1(data, x, y):
    # 保留前x后y
    return data[:x] + data[-y:]

def yangai_rule2(data, x, y):
    # 保留data从第x位至第y位（包含x位，不包含y位）
    # 注意这里x和y是基于0的索引，所以实际提取的是第x+1位到第y位的数据
    return data[x:y]

def yangai_rule3(data, x, y):
    # 遮盖data的前x位和后y位
    # 使用星号 (*) 或其他字符进行遮盖
    masked_data = '*' * x + data[x:-y] + '*' * y
    return masked_data

def yangai_rule4(data, x, y):
    # 遮盖data从第x位至第y位
    # 使用星号 (*) 或其他字符进行遮盖
    masked_section = '*' * (y - x)  # 创建一个长度与要遮盖的部分相同的字符串
    return data[:x] + masked_section + data[y:]

def yangai_rule5(data, x, y):
    # 默认处理逻辑
    return "暂不支持该规则"

def yangai_rule6(data, x, y):
    # 默认处理逻辑
    return "暂不支持该规则"

def yangai_default(data, x, y):
    # 默认处理逻辑
    return "暂不支持该规则"

desensitize_yangai_functions = {
    1: yangai_rule1,
    2: yangai_rule2,
    3: yangai_rule3,
    4: yangai_rule4,
    5: yangai_rule5,
    6: yangai_rule6,
    }

def handle_yangai_request(data):
    print(data)
    name = data.get('name')
    origindata = data.get('origindata')
    yangaiRule = int(data.get('yangaiRule', 0))
    x = int(data.get('x', 0))
    y = int(data.get('y', 0))

    # 获取对应的处理函数
    yangai_function = desensitize_yangai_functions.get(yangaiRule, yangai_default)

    # 应用处理函数
    yangaid_data = yangai_function(origindata, x, y)

    response_data = {
        "result": yangaid_data
    }
    response = {
        'code': 20000,
        'data': response_data
    }
    return response
