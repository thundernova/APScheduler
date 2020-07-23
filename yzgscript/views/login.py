import random
from io import BytesIO
from PIL import Image,ImageDraw,ImageFont
from flask import Blueprint, request, Response, render_template, session, jsonify, redirect, url_for
from datetime import timedelta
from sqlalchemy import func
from ..public import is_login
from ..models import *

blue_login = Blueprint("blue_login",__name__)


#登录验证页面
@blue_login.route("/",methods=['GET','POST'])
@blue_login.route("/login",methods=['GET','POST'])
def login():
    if request.method =='POST':
        username=request.form.get('username')
        password=request.form.get('password')
        validcode=request.form.get('validcode')
        if validcode and validcode.upper()==session['verifycode'].upper():
            loginuser=admin_login.query.filter_by(username=username).first()
            if loginuser and loginuser.is_active==True and loginuser.check_password(password):
                login_success=admin_login_log(login_user=username,login_pass='******',login_ip=request.remote_addr,login_status=True)
                db.session.add(login_success)
                db.session.commit()
                session['loginuser']=loginuser.username
                session['loginpri']=loginuser.is_superuser
                response = {'code': '200', 'msg': '/login_index'}
            else:
                login_failed=admin_login_log(login_user=username,login_pass=password,login_ip=request.remote_addr,login_status=False)
                db.session.add(login_failed)
                db.session.commit()
                response = {'code': '500', 'msg': '登录失败!!!'}
        else:
            response = {'code': '500', 'msg': '验证码错误!!!'}
        session["verifycode"]=''
        return response
    else:
        return render_template('admin_login.html')


# 登录主页框架
@blue_login.route("/login_index")
@is_login
def login_index():
    return render_template("login_index.html",login_user=session.get('loginuser'),login_pri=session['loginpri'])


# 登录后的用户信息页面
@blue_login.route("/login_info")
@is_login
def login_info():
    if request.args.get('action'):
        login_user= session['loginuser']
        login_success = admin_login_log.query.\
            filter(login_user==login_user,admin_login_log.login_status==True).\
            order_by(admin_login_log.id.desc()).first()
        login_failed = admin_login_log.query.\
            filter(login_user==login_user,admin_login_log.login_status==False).\
            order_by(admin_login_log.id.desc()).first()
        if login_failed:
            failed_ip = login_failed.login_ip
            failed_time=str(login_failed.login_time)
        else:
            failed_ip = failed_time = 'None'
        response={'code': '200',
              'login_user':login_user,
              'user_privilege':session['loginpri'],
              'success_ip':login_success.login_ip,
              'success_time':str(login_success.login_time),
              'failed_ip':failed_ip,
              'failed_time':failed_time}
        return response
    else:
        return render_template('login_info.html')


# 登录后的默认主页
@blue_login.route("/login_welcome")
@is_login
def login_welcome():
    if request.args.get('action'):
        my_charts=[]
        users=admin_login.query.count()
        logins=admin_login_log.query.count()
        ops=apscheduler_tasklog.query.count()
        listnum = int(request.values.get('action'))  # 用于告知后端提取最近几天的数据
        charts_name=db.session.query(apscheduler_tasklog.task_status).distinct().all()  # 统计操作日志中在哪几种操作类型
        for i in range(len(charts_name)):
            charts_data = []
            for n in range(0, listnum)[::-1]:             #按ajax提交的最近天数循环
                list_time=((datetime.now() - timedelta(days=n)).strftime("%Y-%m-%d"))  #依次取最近几天的日期
                list_data=db.session.query(apscheduler_tasklog.task_status,func.count(apscheduler_tasklog.task_status)).\
                    filter(apscheduler_tasklog.task_time.contains(list_time),apscheduler_tasklog.task_status==charts_name[i].task_status).\
                    group_by(apscheduler_tasklog.task_status).all()
                if not list_data:
                    list_data=[(charts_name[i].task_status,0)]  #如果没有结果，则默认赋值为0
                charts_data.append(list_data[0][1])  #将最近N次的结果做成列组，其中list_data[0][1]为匹配时间和名称后的统计量。
            mychart_name='成功' if charts_name[i].task_status==True else '失败'
            my_chart={"name":mychart_name,"value":charts_data}  #将名称和最近N天的列表存成类似{"name":'PV',"value":[20,32,11,14,90,30,20,32]}的字典。
            my_charts.append(my_chart)  #将所有操作类型的字典结果再存成列表。
        response={"code":200,"users":users,"logins":logins,"ops":ops,"my_charts":my_charts}
        return response
    else:
        return render_template("login_welcome.html")


# 退出登录
@blue_login.route("/admin_logout")
def logout():
    session['loginuser']=''
    session['loginpri']=''
    return redirect(url_for('blue_login.login'))


# 获取验证码
@blue_login.route("/getvalid")
def getvalid():
    bgcolor = (random.randrange(20, 100), random.randrange(20, 100), 255)
    width = 100
    height = 30
    im = Image.new('RGB', (width, height), bgcolor)
    draw = ImageDraw.Draw(im)
    for i in range(0, 100):  # 调用画笔的point()函数绘制噪点
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)
    str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'  # 定义验证码的备选值
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]
    font = ImageFont.truetype('arial.ttf', 23)  # 构造字体对象，Windows的字体路径为"c:\windows\fonts\下面"
    fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
    draw.text((5, 2), rand_str[0], font=font, fill=fontcolor)
    draw.text((25, 2), rand_str[1], font=font, fill=fontcolor)
    draw.text((50, 2), rand_str[2], font=font, fill=fontcolor)
    draw.text((75, 2), rand_str[3], font=font, fill=fontcolor)
    del draw  # 释放画笔
    session['verifycode'] = rand_str  # 存入session，用于做进一步验证
    buf = BytesIO()  # 内存文件操作
    im.save(buf, 'png')  # 将图片保存在内存中，文件类型为png
    return Response(buf.getvalue(), mimetype='image/png')  # 将内存中的图片数据返回给客户端，MIME类型为图片png


