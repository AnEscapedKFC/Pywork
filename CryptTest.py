import os
import time
import psutil
import base64
from Crypto import Random
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as PKCS1_cipher
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import MainWindow2

global SavePath  # 保存加密后文件存放的位置

import random
import string

def generate_random_string(length=32):
    """生成指定长度的随机字符串"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# 生成一个长度为16的随机字符串


def create_rsa_key():
    random_generator = Random.new().read
    rsa = RSA.generate(2048, random_generator)
    private_key = rsa.exportKey()
    with open("private_a.pem", 'wb') as f:
        f.write(private_key)

    public_key = rsa.publickey().exportKey()
    with open("public_a.pem", 'wb') as f:
        f.write(public_key)

def add_to_16(value):# str不是16的倍数那就补足为16的倍数
    while len(value) % 16 != 0:
        value += '\0'
    return str.encode(value)  # 返回bytes

def encrypt_oracle(file_path):
    # 生成一个随机的16字节初始化向量 (IV)
    iv = get_random_bytes(16)
    random_string = generate_random_string()
    key = random_string
    print(f"key is{key}\n")
    print('\n当被加密文件与本程序不同目录时\n请输入要加密文件完整路径包括文件名以及后缀')
    print('\n当被加密文件与本程序同一目录时只需输入文件名以及后缀：')
    filepath, tempfilename = os.path.split(file_path)  # 将用户提供的文件路径 file_path 拆分为文件所在路径 filepath 和文件名（包含后缀） （tempfilename）
    filename, extension = os.path.splitext(tempfilename)  # 将文件名（包含后缀） tempfilename 拆分为文件名 filename 和文件后缀 extension
    savefile = filename + '已加密' + extension  # 保存加密后文件名称
    savefile = savefile.replace('/', '\\')
    try:
        try:
            virtualmem = psutil.virtual_memory()  # 获取本机内存信息
            availablemem = round(virtualmem.available / 3)
            filesize = os.path.getsize(file_path)
            if filesize > availablemem:
                print("\n\n\n加密文件大于系统可用内存可能影响加密效率或出现内存崩溃\n\n\n")
                print('\n\n是否继续运行 继续操作请按 "y" 返回请按 "n"\n\n')
                temp = input('\n请按键选择')
                if temp == "n" or temp == "N":
                    encrypt_oracle()
        except:
            print('\n输入有误，请重新输入')
            encrypt_oracle()
        text = open(file_path, 'rb').read()  # 待加密文本
        open(file_path, 'rb').close()
    except:
        print('\n输入有误，请重新输入')
        encrypt_oracle()
    text = str(text)  # 转str
    print("加密开始：\n")
    start = time.time()
    # 使用用户提供的密钥初始化加密器和CBC模式
    aes = AES.new(add_to_16(key), AES.MODE_CBC, iv=iv)
    encrypt_aes = aes.encrypt(add_to_16(text))  # 使用加密器对文件内容进行AES加密，生成加密后的内容
    encrypted_text = iv + encrypt_aes  # 包括 IV 在内的加密后内容
    if filepath == "":
        logbat = open(savefile, 'wb')
        logbat.write(encrypted_text)
        logbat.close()
        savepath = "savepath.txt"
        with open(savepath, 'w') as file:
            file.write(savefile)
        print('\n文件加密成功 文件以保存为 ', savefile)
    else:
        Path = filepath + '/' + savefile
        Path = Path.replace('/', '\\')
        #print(MainWindow2.savepath)
        savepath = "savepath.txt"
        with open(savepath, 'w') as file:
            file.write(Path)
        logbat = open(filepath + '\\' + savefile, 'wb')
        logbat.write(encrypted_text)
        logbat.close()
        print('\n文件加密成功 文件保存在 ', filepath, '中 \n\n文件名为 ', savefile)
    # 使用RSA加密key
    with open('public_a.pem') as f:
        public_key = f.read()
        pub_key = RSA.importKey(str(public_key))
        cipher = PKCS1_cipher.new(pub_key)
        rsa_text = base64.b64encode(cipher.encrypt(bytes(key.encode("utf8"))))
    with open("KEY", "wb") as f:
        f.write(rsa_text)  # 保存加密后的密钥
    end = time.time()
    print(f"Spending {end-start} seconds\n")
# 解密方法修改


def decrypt_oralce(file_path, key_path):
    print("开始解密\n")
    f = open("KEY", "rb").read() # 公钥
    private_key = open(key_path, "rb").read()  # 获取私钥
    pri_key = RSA.importKey(private_key)
    cipher = PKCS1_cipher.new(pri_key)
    key = cipher.decrypt(base64.b64decode(f), 0)
    key = key.decode('utf-8')
    print(f"key is：{key}")
    # key = input('\n请输入用于解密文件的秘钥：')
    print('\n当被解密文件与本程序不同目录时\n请输入要解密文件完整路径包括文件名以及后缀')
    print('\n\n当被解密文件与本程序同一目录时只需输入文件名以及后缀：')
    # file_path = input('\n\n请输入：')
    filepath, tempfilename = os.path.split(file_path)
    filename, extension = os.path.splitext(tempfilename)
    try:
        text = open(file_path, 'rb').read()  # 待加密文本
        open(file_path, 'rb').close()
    except:
        print('\n输入有误，请重新输入')
        decrypt_oralce()
    savefile = input('\n请输入解密后文件的名字包括后缀 请不要使用特殊符号：')
    start = time.time()
    # 获取 IV(前16位）
    iv = text[:16]
    text = text[16:] # 除去IV的部分
    # 初始化加密器和CBC模式
    aes = AES.new(add_to_16(key), AES.MODE_CBC, iv=iv)
    base64_decrypted = aes.decrypt(text)
    decrypted_text = base64_decrypted.decode(encoding='gbk').replace('\0', '')  # 执行解密密并转码返回str
    decrypted_text2 = eval(decrypted_text)
    if filepath == "":
        logbat = open(savefile, 'wb')
        logbat.write(decrypted_text2)
        logbat.close()
        print('\n文件解密成功 文件以保存为 ', savefile)
    else:
        logbat = open(filepath + '\\' + savefile, 'wb')
        logbat.write(decrypted_text2)
        logbat.close()
        print('\n文件解密成功 文件保存在 ', filepath, '中 \n\n文件名为 ', savefile)
    end = time.time()
    print(f"Spending {end-start} seconds")


if __name__ == '__main__':
    encrypt_oracle("1.txt")
    decrypt_oralce("1已加密.txt","private_a.pem")


