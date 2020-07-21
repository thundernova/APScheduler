from .exts import db
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash

class admin_login(db.Model):
    id=db.Column(db.Integer,comment='ID',primary_key=True,nullable=False,autoincrement=True)
    username=db.Column(db.String(32),comment='账号名称',unique=True)
    email=db.Column(db.String(32),comment='账号邮箱')
    adminpwd=db.Column(db.String(128),comment='账号密码')
    is_superuser=db.Column(db.Boolean,comment='账号权限(0为管理员,1为超管)',default='0')
    is_active=db.Column(db.Boolean,comment='账号状态(0为禁用,1为启用)',default='0')
    @property
    def password(self):
        raise Exception("Password Can't be Access!!!")
    @password.setter
    def password(self,value):
        self.adminpwd=generate_password_hash(value)
    def check_password(self,password):
        return check_password_hash(self.adminpwd,password)

class admin_login_log(db.Model):
    id=db.Column(db.Integer,comment='ID',primary_key=True)
    login_user=db.Column(db.String(32),comment='登录用户')
    login_pass=db.Column(db.String(128),comment='登录密码',nullable=True)
    login_ip=db.Column(db.String(15),comment='登录IP')
    login_time=db.Column(db.DateTime,comment='登录时间',default=datetime.now)
    login_status =db.Column(db.Boolean,comment='登录状态',default='True')
    def __str__(self):
        return 'admin_login_log{id=%s}' % (self.id)

class apscheduler_tasklog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.String(16))
    task_cmd = db.Column(db.String(128))
    task_time = db.Column(db.DateTime, default=datetime.now)
    task_status = db.Column(db.Boolean)
    task_stdout = db.Column(db.Text)
    def to_json(self):
        json_post = {
            'id': self.id,
            'task_id': self.task_id,
            'status': self.status,
            #'exe_time': datetime.strftime(self.exe_time, '%Y-%m-%d'),
            'exe_time': self.exe_time,
            'cmd': self.cmd,
            'stdout': self.stdout
        }
        return json_post