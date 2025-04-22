import os




class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))  # 项目根目录
    # 使用 MySQL 数据库
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:666666@localhost/app?charset=utf8mb4'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

