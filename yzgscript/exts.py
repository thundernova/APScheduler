from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from flask_apscheduler import APScheduler

db = SQLAlchemy()
migrate=Migrate()
scheduler=APScheduler()

# 初始化扩展库
def init_ext(app):
    db.init_app(app)          # 初始化数据库
    db.app = app
    migrate.init_app(app,db)  # 初始化数据库迁移插件
    CSRFProtect(app)          # 开启CSRF保护
    scheduler.init_app(app)   # 初始化计划任务框架
    scheduler.start()         # 开启计划任务
    # DEBUG模式用到了Werkzeug库，它生成的子进程用于监测代码变动就自动重启，所以会导致执行两次定时任务。