from flask import Blueprint, request, render_template, session
from ..models import *
from ..public import is_login,to_json

blue_userlog = Blueprint("blue_userlog",__name__)


# 列出所有日志
@blue_userlog.route("/admin_userlog",methods=['GET','POST'])
@is_login
def admin_loglist():
    if request.args.get('action'):
        page=request.args.get('page',1,type=int)
        per_page=request.args.get('limit',10,type=int)
        if session['loginpri']:
            data_list=admin_login_log.query.all()
        else:
            data_list=admin_login_log.query.filter(admin_login_log.login_user==session['loginuser']).all()
        start=(page-1)*per_page
        end=page * per_page if len(data_list) > page * per_page else len(data_list)
        page_data=[data_list[i] for i in range(start,end)]
        data={"code":'0',"count":len(data_list),"data":to_json(page_data)}
        return data
    else:
        return render_template('admin_userlog.html')
