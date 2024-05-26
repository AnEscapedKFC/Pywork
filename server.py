"""
后端功能测试
"""
from flask import Flask, request, jsonify
from flask_mail import Message
import pwdtest
import hashlib
import config1
from db4 import Person, PersonAddress, EmailCaptchaModel
import Forms
import string
import random
from datetime import datetime
from flask_mail import Mail
from exts import db
import ServerFunctions
import codecs
app = Flask(__name__)
app.config.from_object(config1)  # 自动读取配置信息
mail = Mail(app)  # 创建mail实例（与app绑定！）
db.init_app(app)  # 从别的模块导入的db实例，需要与与app进行绑定！！！
pkey = ' '   # 全局变量，保存当前用户的私钥地址


@app.route('/api', methods=['POST','GET'])
def handle_request():
    data = request.json  # 获取从 PyQt5 应用程序发送的 JSON 数据
    username = data.get('user')  # 获取用户名字段
    password = data.get('password')  # 获取密码字段
    address = data.get('address')
    private_key = data.get('private_key')
    if username is not None and password is not None:
        # 在此处进行处理并返回响应给 PyQt5 应用程序
        response_data = {
            'message': f'用户名是{username}，密码是{password},账号地址是{address}，账号私钥是{private_key}'
        }
        return jsonify(response_data.get('message'))
    else:
        # 如果未提供有效的消息字段，返回错误响应
        return jsonify({'error': 'Invalid data format'}), 400


@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.json
        username = data.get('username')  # 获取用户名字段
        password = data.get('password')  # 获取密码字段
        address = data.get('address')
        private_key = data.get('private_key')
        email = data.get('email')
        captcha = data.get('captcha')  # 获取验证码
        if username is None or password is None or address is None or private_key is None or email is None or captcha is None:
            return jsonify({"error": "All fields are required."}), 400
        hashed_value = pwdtest.hash_string(password)  # 将用户输入的密码映射为32位定长字符串
        pwd1 = hashed_value[:16]  # hash(pwd1): 用于校验用户设置的一级密码
        pwd2 = hashed_value[16:]  # hash(pwd2): 用于充当AES加密私钥地址的密钥
        encrypted_pwd2 = pwdtest.encrypt_oracle(sc=private_key, key=pwd2)  # 密文私钥地址，存放在数据库PersonAddress中
        encrypted_pwd2 = str(encrypted_pwd2)  # !!!!!!!!!!!!!!!一定要转为str类型！！！！！！！！！！！！
        print(f"encrypted_pwd2 is {encrypted_pwd2}")
        # 进行后端数据验证
        Forms.validate_email(email=email)  # 验证邮箱是否已被注册
        Forms.validate_captcha(email=email, captcha=captcha)  # 验证验证码是否正确
        if not ServerFunctions.keys_match(address, private_key):
            return jsonify({"code": 500, "message": "Address and private key do not match!", "data": None})
        user = Person(email=email, username=username, pwd1=pwd1, pwd2=pwd2, address=address, money=0.00)  # 创建user对象
        p_address = PersonAddress(username=username, public_key=address, private_key=encrypted_pwd2)  # 存储加密后的区块链私
        with app.app_context():
            db.session.add(user)  # 向数据库添加
            db.session.add(p_address)
            db.session.commit()  # 提交事务
            return jsonify({"code": 200, "message": "Registration successful!", "data": None})
    except Exception as e:
        # 出现异常时返回错误信息
        return jsonify({"error": str(e)}), 500


@app.route("/login", methods=['POST'])
def login():
    try:
        data = request.json
        username = data.get('username')  # 获取用户名字段
        print(username)
        password = data.get('pwd')  # 获取密码字段
        print(password)
        password = str(password)  #
        hashed_value = pwdtest.hash_string(password)  # 映射为32位定长字符串
        print(hashed_value)
        pwd1 = hashed_value[:16]  # hash(pwd1): 用于校验用户设置的一级密码
        pwd2 = hashed_value[16:]  # AES密钥
        print(f"pwd1 is {pwd1}")
        print(f"pwd2 is {pwd2}")
        with app.app_context():
            user = db.session.query(PersonAddress).filter_by(username=username).first()   # 获取当前用户的地址数据
            address = str(user.public_key)
            encrypted_private_key = str(user.private_key)  # AES加密后的私钥地址,此处为str类型
            person = db.session.query(Person).filter_by(username=username, address=address).first()  # 获取当前用户数据
            person_pwd1 = str(person.pwd1)  # 获取存储在数据库中的用户的pwd1,与用户输入的密码进行对比
            print(person_pwd1)
            if person_pwd1 != pwd1:
                return jsonify({"error": "密码错误"}), 500  # 密码错误，返回500状态码
            print(f"enkey is {encrypted_private_key}")
            new_bytes = bytes(encrypted_private_key[2:-1], encoding="utf-8")  # 这是bytes类型
            print(f"new_bytes is {new_bytes}")
            original = codecs.escape_decode(new_bytes, "hex-escape")
            print(original)  # tuple
            print(type(original[0]))  # 得到正确的bytes类型数据
            private_key = pwdtest.decrypt_oralce(key=pwd2, PWD2=original[0])  # 对私钥地址进行解密,返回私钥地址
            global pkey
            pkey = private_key
            return jsonify({"code": 200, "message": "login successfully", "data": None})  # f返回json格式的字符串

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/info", methods=['POST'])
def info():
    pass


@app.route("info/userinfo", methods=['POST', 'GET'])
def userinfo():
    data = request.json
    username = data.get('username')
    money = db.session.query(Person).filter_by(username=username).first()  # 查询用户余额


@app.route("/email", methods=['POST','GET'])
def get_email_captcha():
    data = request.json  # 获取从 PyQt5 应用程序发送的 JSON 数据
    email = data.get('email')
    print(email)
    # 4/6: 随机数组、宁母、数组和字母的组合
    source = string.digits*4
    captcha = random.sample(source, 4)  # 从source中随机取四位
    # print(captcha)
    captcha = "".join(captcha)  # 转字符串
    message = Message(subject="平台验证码", recipients=[email], body=f"您的验证码是{captcha}")
    mail.send(message)  # 发送验证码
    # 该操作较为耗时一般交给另外一个进程
    # memcached/redis
    # 用数据库表的方式存储
    email_captcha = EmailCaptchaModel(email=email,captcha=captcha,time=datetime.now())
    db.session.add(email_captcha)  # 添加到数据库
    db.session.commit()
    # RESTful API
    return jsonify({"code": 200, "message": "", "data": None})  # f返回json格式的字符串


# if __name__ == '__main__':
#     app.run(debug=True)






  #U