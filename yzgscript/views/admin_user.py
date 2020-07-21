from flask import Blueprint, request, render_template, session
from distutils.util import strtobool
from ..models import *
from ..public import is_login,to_json

blue_user = Blueprint("blue_user",__name__)


# 列出所有用户
@blue_user.route("/admin_user",methods=['GET','POST'])
@is_login
def admin_user():
    if request.args.get('action'):
        reloadname=request.args.get('reloadname')
        page=request.args.get('page',1,type=int)
        per_page=request.args.get('limit',10,type=int)
        if session['loginpri']:
            if reloadname:
                data_list=admin_login.query.filter(admin_login.username.contains(reloadname)).all()
            else:
                data_list=admin_login.query.all()
        else:
            data_list=admin_login.query.filter(admin_login.username==session['loginuser']).all()
        start=(page-1)*per_page
        end=page * per_page if len(data_list) > page * per_page else len(data_list)
        page_data=[data_list[i] for i in range(start,end)]
        response={"code":'0',"loginpri":session['loginpri'],"count":len(data_list),"data":to_json(page_data)}
        return response
    else:
        return render_template('admin_user.html',loginpri=session['loginpri'])


# 新增、修改、查看操作
@blue_user.route("/admin_useraction",methods=['GET','POST'])
@is_login
def admin_useraction():
    response = {'code': '500'}
    dataid=request.values.get('dataid')
    if dataid:    #根据ID查出相关信息，防止用户提交修改过的POST信息。
        data_info=admin_login.query.filter_by(id=dataid).first()
    # 处理新增或修改完成后的提交数据。
    if request.method == 'POST':
        admin_name=request.values.get('admin_name')
        admin_email=request.values.get('admin_email')
        admin_pass=request.values.get('admin_pass')
        admin_super=strtobool(request.values.get('admin_super')) if request.values.get('admin_super') else data_info.is_superuser
        admin_status=strtobool(request.values.get('admin_status')) if request.values.get('admin_status') else data_info.is_active
        data_exist=admin_login.query.filter(admin_login.username==admin_name).first()
        if dataid:   #如果存在dataid，则编辑。
            if (data_info.username != admin_name and data_exist):  # 修改了名称。
                response = {"code": '201', "msg": "用户已存在!!!"}
            else:
                update_data=admin_login.query.get(dataid)
                update_data.username=admin_name
                update_data.email=admin_email
                update_data.is_superuser=admin_super
                update_data.is_active=admin_status
                if data_info.adminpwd!=admin_pass:   #修改了密码
                    update_data.password=admin_pass
                db.session.commit()
                response = {"code": '200', "msg": "修改用户成功!"}
        else:  #新增用户。
            if data_exist:
                response = {"code": '201', "msg": "用户已存在!!!"}
            else:
                admin_add=admin_login(username=admin_name,email=admin_email,password=admin_pass,is_superuser=admin_super,is_active=admin_status)
                db.session.add(admin_add)
                db.session.commit()
                response = {"code": '200', "msg": "添加用户成功!"}
        return response
    else:  # 打开新增、查看、修改用户请求页面。
        if dataid:   # 查看、修改，需回传相关信息参数。
            data_info.action=request.values.get('action')
            data_info.pri=session['loginpri']
            return render_template("admin_useraction.html", data_info=data_info)
        else:          # 新增，不需要传参数。
            return render_template("admin_useraction.html")


# 用户删除、停用、启用操作
@blue_user.route("/admin_userop",methods=['GET','POST'])
@is_login
def admin_userop():
    response = {'code': '500'}
    dataid=request.values.get('dataid').split(',')
    adminop=request.values.get('action')
    try:
        if session['loginpri']:
            if (adminop=='del'):
                admin_login.query.filter(admin_login.id.in_(dataid)).delete(synchronize_session=False)
                response['msg'] = "ID [%s] del success!" % dataid
            elif (adminop=='start'):
                admin_login.query.get(dataid).is_active=1
                response['msg'] = "ID [%s] start success!" % dataid
            else:
                admin_login.query.get(dataid).is_active=0
                response['msg'] = "ID [%s] stop success!" % dataid
            db.session.commit()
            response['code'] = 200
        else:
            response = {"code": '403', "msg": "权限拒绝!!!"}
    except Exception as e:
        response = {"code": '500', "msg": str(e)}
    return response