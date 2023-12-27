from gmssl import sm4
import base64
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES

from gmssl import sm4, func

def sm4_encrypt(key, data, mode="ECB", padding='PKCS7Padding', iv="abcdef0123456789", output_format='base64'):
    """
    使用SM4算法加密数据。
    :param key: 加密密钥（16字节）。
    :param data: 要加密的明文。
    :param mode: 加密模式（ECB, CBC, CFB, CTR, OFB）。
    :param padding: 填充方式（NoPadding, PKCS5Padding, PKCS7Padding）。
    :param iv: 一些模式下所需的初始化向量（16字节）。
    :param output_format: 输出格式（'base64' 或 'hex'）。
    :return: 加密数据（Base64或Hex格式）。
    """
    if padding in ['PKCS5Padding', 'PKCS7Padding']:
        block_size = 16
        data = pad(data.encode(), block_size, style='pkcs7')
    else:
        print("对data进行编码")
        data = data.encode()

    crypt_sm4 = sm4.CryptSM4()

    if mode == 'ECB':
        crypt_sm4.set_key(key.encode(), sm4.SM4_ENCRYPT)
        encrypted_data = crypt_sm4.crypt_ecb(data)
    elif mode == 'CBC':
        crypt_sm4.set_key(key.encode(), sm4.SM4_ENCRYPT)
        encrypted_data = crypt_sm4.crypt_cbc(iv.encode(), data)
    # 其他模式的实现可能需要根据gmssl库的具体支持进行调整
    else:
        raise ValueError(f"Unsupported mode: {mode}")

    if output_format == 'base64':
        return base64.b64encode(encrypted_data).decode()
    elif output_format == 'hex':
        return encrypted_data.hex()
    else:
        raise ValueError(f"Unsupported output format: {output_format}")

# 示例使用
# key = "012345678cdef"  # 16字节的密钥
# data = "Sensitive Information"
# iv = "abcdef0123456789" 
# encrypted_data = sm4_encrypt(key, data, mode="CBC",iv=iv,padding='PKCS7Padding', output_format='hex')
# print(encrypted_data)

def sm4_encrypt_api(json_data):
    print(json_data)
    try:
        key = json_data.get('key')
        data = json_data.get('data')
        mode = json_data.get('mode')
        padding = json_data.get('padding', 'PKCS7Padding')
        iv = json_data.get('iv', "abcdef0123456789")
        output_format = json_data.get('output_format', 'base64')

        # 检查密钥和IV长度（对于SM4，密钥应为16字节）
        if len(key) != 16 or (iv is not None and len(iv) != 16):
            response_data = {
                "result": "Error, Key and IV must be 16 bytes long for SM4."
            }
            response = {
                'code': 20000,
                'data': response_data
            }
            return response

        # 调用SM4加密函数
        encrypted_data = sm4_encrypt(key, data, mode, padding, iv, output_format)
        response_data = {
            "result": encrypted_data
        }
        response = {
            'code': 20000,
            'data': response_data
        }
        return response
    except Exception as e:
        response_data = {
            "result": str(e)
        }
        response = {
            'code': 20000,
            'data': response_data
        }
        return response

# # 示例用法
# json_input = {
#     "key": "01234567abcdef",
#     "data": "Sensitive Information",
#     "mode": "ECB",
#     "iv": "abcdef0123456789",
#     "output_format": "hex"
# }
# response = sm4_encrypt_api(json_input)
# print(response)


def sm4_encrypt_easy(key, data):
    """
    使用SM4算法加密数据
    :param key: 16字节的密钥
    :param data: 要加密的数据
    :return: 加密后的数据
    """
    crypt_sm4 = sm4.CryptSM4()
    crypt_sm4.set_key(key.encode(), sm4.SM4_ENCRYPT)
    encrypted_data = crypt_sm4.crypt_ecb(data.encode())  # ECB模式
    return func.bytes_to_list(encrypted_data)

def sm4_sensitive_data_masking(key, sensitive_data):
    """
    对敏感数据进行脱敏处理
    :param key: 16字节的密钥
    :param sensitive_data: 需要脱敏的敏感数据
    :return: 脱敏后的数据
    """
    return sm4_encrypt(key, sensitive_data)

# # 示例
# key = "0123456789abcdef"  # 密钥
# data = "Sensitive Information"  # 敏感信息
# masked_data = sm4_sensitive_data_masking(key, data)
# print(masked_data)

def sm4_decrypt_easy(key, encrypted_data):
    """
    使用SM4算法解密数据
    :param key: 16字节的密钥
    :param encrypted_data: 加密过的数据
    :return: 解密后的数据
    """
    crypt_sm4 = sm4.CryptSM4()
    crypt_sm4.set_key(key.encode(), sm4.SM4_DECRYPT)
    decrypted_data = crypt_sm4.crypt_ecb(func.list_to_bytes(encrypted_data))  # ECB模式
    return decrypted_data.decode()

# decrypted_data = sm4_decrypt(key, masked_data)
# print(decrypted_data)

