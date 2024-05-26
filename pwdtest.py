"""
密码设计思想：
person表设置两个密码列，分别为一级密码与二级密码。
用户在注册时，输入一个字符串作为密码，后端接受密码后，使用哈希算法将其映射为一个32位的string，其中前十六位作为hash（pwd1），存放在pwd1列中。后十六位hash（pwd2），作为AES的密钥，加密用户的区块私钥地址sc，密文存放在pwd2列中。
用户在登录时，输入自己设定的密码，后端接受后，采用相同的哈希算法将其转为32位字符串，前十六位与pwd1列中的数据比较，若通过，则将后十六位与用户对应的密文传给解密函数，解密后得到私钥地址sc。

注意事项！！！：str与bytes类型的转化，直接使用encode方式对str类型的字符串进行转换时，会对 \ 进行转义，并且再加上一重b''标识，无法得到正确结果，无法执行解密函数。
为解决这个问题，首先应对字符串进行切片【2：-1】，得到new_bytes再使用codecs.escape_decode(new_bytes, "hex-escape")，得到元组，元组的第一项就是正确的bytes数据!!!
具体原理详见：http://t.csdnimg.cn/xt3v3

"""
import hashlib
import time
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import pymysql
import codecs
# 以下库为测试函数调用的库，完工后可删除
from db4 import Person, PersonAddress, EmailCaptchaModel
from exts import db
import config1
from flask import Flask, request, jsonify
from flask_mail import Message


def hash_string(input_string):
    # 创建SHA-256哈希对象
    sha256 = hashlib.sha256()
    # 更新哈希对象的内容
    sha256.update(input_string.encode('utf-8'))
    # 获取十六进制表示的哈希值
    hashed_str = sha256.hexdigest()
    # 返回定长的哈希值
    return hashed_str[:32]  # 取前32个字符作为定长哈希值


def add_to_16(value):  # str不是16的倍数那就补足为16的倍数
    while len(value) % 16 != 0:
        value += '\0'
    return str.encode(value)  # 返回bytes


def encrypt_oracle(sc, key):
    # 生成一个随机的16字节初始化向量 (IV)
    iv = get_random_bytes(16)
    print(f"key is {key}\n")
    start = time.time()
    # 使用用户提供的密钥初始化加密器和CBC模式
    aes = AES.new(add_to_16(key), AES.MODE_CBC, iv=iv)
    encrypt_aes = aes.encrypt(add_to_16(sc))  # 使用加密器对文件内容进行AES加密，生成加密后的内容
    encrypted_text = iv + encrypt_aes  # 包括 IV 在内的加密后内容
    print(f"加密后的sc为{encrypted_text}")
    # str_data = encrypted_text.decode('gbk')
    # print(str_data)
    end = time.time()
    print(f"Spending {end-start} seconds\n")
    return encrypted_text


def decrypt_oralce(key, PWD2):
    print(f"key is：{key}")
    text = PWD2  # 待加密文本
    start = time.time()
    # 获取 IV(前16位）
    iv = text[:16]
    text = text[16:]  # 除去IV的部分
    # 初始化加密器和CBC模式
    aes = AES.new(add_to_16(key), AES.MODE_CBC, iv=iv)
    base64_decrypted = aes.decrypt(text)
    decrypted_text = base64_decrypted.decode(encoding='gbk').replace('\0', '')  # 执行解密密并转码返回str
    print(f"sc为：{decrypted_text}")
    end = time.time()
    print(f"Spending {end-start} seconds")
    return decrypted_text


# 示例用法

if __name__ == '__main__':
    app = Flask(__name__)
    app.config.from_object(config1)  # 自动读取配置信息
    db.init_app(app)  # 从别的模块导入的db实例，需要与app进行绑定！！！
    with app.app_context():
        input_str = "1234"
        hashed_value = hash_string(input_str)
        pwd1 = hashed_value[:16]  # hash(pwd1): 用于校验用户设置的一级密码
        pwd2 = hashed_value[16:]
        print(f"pwd1 is {pwd1}")
        print(f"pwd2 is {pwd2}")
        PWD2 = encrypt_oracle(sc="0xc041842F37395A7C58Af34a528efB20586f05785",
                              key=pwd2)  # 密文，存放在数据库中!!!!!!!!!!!bytes类型
        PWD2 = str(PWD2)
        print(f"str is {PWD2}")
        new_bytes = bytes(PWD2[2:-1], encoding="utf-8")  # 这是bytes类型
        print(f"new_bytes is {new_bytes}")
        original = codecs.escape_decode(new_bytes, "hex-escape")
        print(original)  # tuple
        print(type(original[0]))  # 得到正确的bytes类型数据
        sc = decrypt_oralce(key=pwd2, PWD2=original[0])  # !待解决，\转义问题！！！！！！！！！!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        # username = 'KFC'
        # user = db.session.query(PersonAddress).filter_by(username=username).first()  # 获取当前用户的地址数据
        # Pwd2 = db.session.query(Person).filter_by(username=username).first()
        # pwd2 = str(Pwd2.pwd2)  # pwd2, AES密钥
        # print(pwd2)
        # encrypted_private_key = str(user.private_key)  # AES加密后的私钥地址,此处为str类型
        # encrypted_private_key = encrypted_private_key.encode('utf-8')  # 转为bytes类型，准备解密
        # print(f"enk is {encrypted_private_key}")
        # pkey = decrypt_oralce(key=pwd2, PWD2=encrypted_private_key)
        # print(pkey)



