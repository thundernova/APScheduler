import os
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = '#KJE)@#JDJIJE)JE@J'
    SQLALCHEMY_TRACK_MODIFICATIONS= False
    SQLALCHEMY_ECHO = False

    # 邮件信息
    MAIL_SUBJECT_PREFIX = '<任务系统>'
    MAIL_SENDER = '任务系统 <it@xxx.com>'
    MAIL_PORT = 465
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'ops@xxx.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or '123456'

    # apscheduler 配置信息
    # JOBS = [{'id': 'job1','func': 'yzgscript.views.scheduler_tasks:job1','trigger': 'interval','seconds': 1}]
    JOBS = [ ]
    SCHEDULER_EXECUTORS = {
        'default': {'type': 'threadpool', 'max_workers': 20}
    }
    SCHEDULER_JOB_DEFAULTS = {
        'coalesce': False, 'max_instances': 5
    }
    SCHEDULER_API_ENABLED = True

    MAX_CONTENT_LENGTH = 8 * 1024 * 1024
    UPLOADED_PHOTOS_DEST = os.path.join(BASE_DIR, 'static/uploads')

    # 配置类可以定义 init_app() 类方法，其参数是程序实例。
    # 在这个方法中，可以执行对当前 环境的配置初始化。
    # 现在，基类 Config 中的 init_app() 方法为空。
    @staticmethod
    def init_app(app):
        pass

class DEV(Config):
    DEBUG = True
    DB_INFO={
        'user':'root',
        'pass':'rootpwd',
        'host':'127.0.0.1',
        'port':3306,
        'db':'yzgscript'
    }
    #SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR,'data-dev.sqlite')
    SQLALCHEMY_DATABASE_URI= 'mysql://%s:%s@%s:%s/%s?charset=utf8' %(
        DB_INFO['user'],DB_INFO['pass'],DB_INFO['host'],DB_INFO['port'],DB_INFO['db']
    )
    SCHEDULER_JOBSTORES = {
        'default': SQLAlchemyJobStore(url='mysql+pymysql://%s:%s@%s:%s/%s?charset=utf8' %(
            DB_INFO['user'],DB_INFO['pass'],DB_INFO['host'],DB_INFO['port'],DB_INFO['db']
        ))
    }

class PRO(Config):
    DB_INFO={
        'user':'root',
        'pass':'rootpwd',
        'host':'172.16.250.78',
        'port':3306,
        'db':'yzgscript'
    }
    SQLALCHEMY_DATABASE_URI= 'mysql://%s:%s@%s:%s/%s?charset=utf8' %(
        DB_INFO['user'],DB_INFO['pass'],DB_INFO['host'],DB_INFO['port'],DB_INFO['db']
    )
    SCHEDULER_JOBSTORES = {
        'default': SQLAlchemyJobStore(url='mysql+pymysql://%s:%s@%s:%s/%s?charset=utf8' %(
            DB_INFO['user'],DB_INFO['pass'],DB_INFO['host'],DB_INFO['port'],DB_INFO['db']
        ))
    }

config = { 'dev': DEV,'pro': PRO,'default': DEV }