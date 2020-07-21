import functools
from flask import session, redirect, url_for

# 判断是否登录
def is_login(func):
    @functools.wraps(func)       #修饰内层函数，防止当前装饰器去修改被装饰函数的属性
    def inner(*args, **kwargs):  #从session获取用户信息，如果有，则用户已登录，否则没有登录
        loginuser = session.get('loginuser')
        if not loginuser:
            return redirect(url_for('op_login.login'))
        return func(*args, **kwargs)
    return inner

# 把结果转为json格式
def to_json(data):
    result = []
    for comment in data:
        dict = comment.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        result.append(dict)
    return result

