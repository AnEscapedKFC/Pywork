import os
USERNAME = 'root'  # 设置登录账号
PASSWORD = '1234'  # 设置登录密码
HOST = '127.0.0.1'  # 设置主机地址
PORT = '3306'  # 设置端口号
DATABASE ='db_5'  # 设置访问的数据库
# 创建URI（统一资源标志符）
'''
SQLALCHEMY_DATABASE_URI的固定格式为：
'{数据库管理系统名}://{登录名}:{密码}@{IP地址}:{端口号}/{数据库名}?charset={编码格式}'
'''
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME, PASSWORD, HOST, PORT, DATABASE)

# 设置数据库的连接URI
SQLALCHEMY_DATABASE_URI = DB_URI
# 设置动态追踪修改,如未设置只会提示警告
SQLALCHEMY_TRACK_MODIFICATIONS = False
# 设置查询时会显示原始SQL语句
SQLALCHEMY_ECHO = False


# 邮箱配置信息：
MAIL_SERVER = "smtp.qq.com"
MAIL_USE_SSL = True
MAIL_PORT = 465
MAIL_USERNAME = "2061398880@qq.com"  # 更改为自己的邮箱账号
MAIL_PASSWORD = "xcplhuamlhnkchij"  # SMTP授权码
MAIL_DEFAULT_SENDER = "2061398880@qq.com"
SECRET_KEY = os.urandom(24)
SECRET_KE = "fafadgrawewga"
