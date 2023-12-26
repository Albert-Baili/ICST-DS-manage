from Cryptodome.Cipher import DES
from Cryptodome.Util.Padding import pad, unpad
from Cryptodome.Random import get_random_bytes
import base64

from gmssl import sm4, func

def des_encrypt(key, data, mode, padding='PKCS5Padding', iv=None):
    """
    使用DES算法加密数据。

    :param key: 加密密钥（8字节）。
    :param data: 要加密的明文。
    :param mode: 加密模式（ECB, CBC, CFB, CTR, OFB）。
    :param padding: 填充方式（NoPadding, PKCS5Padding, PKCS7Padding）。
    :param iv: 一些模式下所需的初始化向量（8字节）。
    :return: 加密数据（Base64格式）。
    """
    # 如果需要，进行填充
    if padding in ['PKCS5Padding', 'PKCS7Padding']:
        data = pad(data.encode(), DES.block_size)
    else:
        data = data.encode()

    # 选择加密模式
    if mode == 'ECB':
        cipher = DES.new(key, DES.MODE_ECB)
    elif mode == 'CBC':
        cipher = DES.new(key, DES.MODE_CBC, iv)
    elif mode == 'CFB':
        cipher = DES.new(key, DES.MODE_CFB, iv)
        
    elif mode == 'CTR':
        nonce = iv[:8]
        cipher = DES.new(key, DES.MODE_CTR, nonce=nonce)
    elif mode == 'OFB':
        cipher = DES.new(key, DES.MODE_OFB, iv)
    else:
        raise ValueError("无效的模式")

    # 加密
    encrypted_data = cipher.encrypt(data)

    # 编码为Base64
    return base64.b64encode(encrypted_data).decode()

def des_decrypt(key, data, mode, padding='PKCS5Padding', iv=None):
    """
    使用DES算法解密数据。

    :param key: 解密密钥（8字节）。
    :param data: 加密数据（Base64格式）。
    :param mode: 解密模式（ECB, CBC, CFB, CTR, OFB）。
    :param padding: 填充方式（NoPadding, PKCS5Padding, PKCS7Padding）。
    :param iv: 一些模式下所需的初始化向量（8字节）。
    :return: 解密后的明文。
    """
    # 从Base64解码
    encrypted_data = base64.b64decode(data)

    # 选择解密模式
    if mode == 'ECB':
        cipher = DES.new(key, DES.MODE_ECB)
    elif mode == 'CBC':
        cipher = DES.new(key, DES.MODE_CBC, iv)
    elif mode == 'CFB':
        cipher = DES.new(key, DES.MODE_CFB, iv)
    elif mode == 'CTR':
        nonce = iv[:8]
        cipher = DES.new(key, DES.MODE_CTR, nonce=nonce)
    elif mode == 'OFB':
        cipher = DES.new(key, DES.MODE_OFB, iv)
    else:
        raise ValueError("无效的模式")

    # 解密
    decrypted_data = cipher.decrypt(encrypted_data)

    # 如果需要，去除填充
    if padding in ['PKCS5Padding', 'PKCS7Padding']:
        decrypted_data = unpad(decrypted_data, DES.block_size)

    return decrypted_data.decode()

key = b'12345678'  # 8字节密钥
iv = get_random_bytes(8)  # 8字节IV
data = "testdata"

def sm4_encrypt(key, data):
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

# 示例
key = "0123456789abcdef"  # 密钥
data = "Sensitive Information"  # 敏感信息
masked_data = sm4_sensitive_data_masking(key, data)
print(masked_data)

def sm4_decrypt(key, encrypted_data):
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

decrypted_data = sm4_decrypt(key, masked_data)
print(decrypted_data)

# encrypted_data = des_encrypt(key, data, mode='ECB', padding='PKCS5Padding', iv=iv)

# decrypted_data = des_decrypt(key, encrypted_data, mode='ECB', padding='PKCS5Padding', iv=iv)

# print(encrypted_data, decrypted_data)

