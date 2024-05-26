# coding: utf-8
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, render_template, jsonify
import config1
from sqlalchemy import Column, DECIMAL, DateTime, Float, Integer, String, Table, text
from sqlalchemy.dialects.mysql import TEXT, VARCHAR
from sqlalchemy.ext.declarative import declarative_base
from exts import db
from datetime import datetime
Base = declarative_base()
metadata = Base.metadata


class GoodsInformation(Base):
    __tablename__ = 'goods_information'

    owner = Column(VARCHAR(255), nullable=False)
    name = Column(VARCHAR(255), nullable=False)
    size = Column(Float(asdecimal=True), nullable=False)
    time = Column(DateTime)
    good_hash = Column(VARCHAR(255), primary_key=True, nullable=False)
    price = Column(DECIMAL(10, 2))
    Key_Word = Column(VARCHAR(255), nullable=False)
    isForsale = Column(VARCHAR(255), nullable=False)
    id = Column(Integer, primary_key=True, nullable=False)
    pkey_hash = Column(VARCHAR(255), nullable=False)
    MerkleTree_hash = Column(VARCHAR(255), nullable=False)
    key_hash = Column(String(255), nullable=False)


class Person(Base):
    __tablename__ = 'person'

    username = Column(String(255))
    pwd1 = Column(String(255))  # 一级密码，取前16位hash组成
    pwd2 = Column(String(255))  # 二级密码，AES加密sc的私钥
    address = Column(String(255), primary_key=True, nullable=False)
    money = Column(DECIMAL(10, 2), server_default=text("'0.00'"))
    email = Column(String(255), nullable=False)


class PersonAddress(Base):
    __tablename__ = 'person_address'

    username = Column(String(255), nullable=False)
    public_key = Column(String(255), primary_key=True, nullable=False)
    private_key = Column(String(255))


class Transcation(Base):
    __tablename__ = 'transcation'
    seller = Column(VARCHAR(255))
    buyer = Column(VARCHAR(255))
    good_name = Column(TEXT)
    time = Column(DateTime)
    price = Column(String(255))
    tradehash = Column(VARCHAR(255), primary_key=True)


class EmailCaptchaModel(db.Model):  # 邮箱类
    __tablename__ = "email_captcha"
    id = db.Column(db.Integer,primary_key=True, autoincrement=True, default=0)  # 自增
    email = db.Column(db.String(100),nullable=False)
    captcha = db.Column(db.String(100),nullable=False)
    time = Column(DateTime, default=datetime.now)
    used = db.Column(db.Boolean,default=False)  # 是否已经被使用


# app = Flask(__name__)
# # 在app.config中设置好数据库配置信息
# app.config.from_object(config1)  # 自动读取配置信息
# db = SQLAlchemy(app)
# email = "1111"
# username = '1dwdw00'
# pwd1 = '1'
# pwd2 = '2'
# address = 'wffwfw0111'
# encrypted_pwd2 = 'ssss1'

# with app.app_context():
#     db.create_all()
#     first_person = db.session.query(Person).all()
#     user = db.session.query(Person).filter_by(email=email).all()
#     user1 = Person(email=email, username=username, pwd1=pwd1, pwd2=pwd2, address=address, money=0.00)  # 创建user对象
#     p_address = PersonAddress(username=username, public_key=address, private_key=encrypted_pwd2)  # 存储加密后的区块链私钥
#     print(1)
#     db.session.add(user1)
#     db.session.add(p_address)
#     db.session.commit()
    # print(user)
    # print(user1.email)
    # print(1)
    # for person in first_person:
    #     print(f"用户余额为：{person.money}")
    # person_address = db.session.query(PersonAddress).all()
    # for persona in person_address:
    #     print(persona)