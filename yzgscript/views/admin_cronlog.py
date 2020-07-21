from flask import Blueprint, request, render_template
from ..models import *
from ..public import is_login,to_json

blue_cronlog = Blueprint("blue_cronlog",__name__)


# 列出所有日志
@blue_cronlog.route("/admin_cronlog",methods=['GET','POST'])
@is_login
def admin_cronlog():
    if request.args.get('action'):
        page=request.args.get('page',1,type=int)
        per_page=request.args.get('limit',10,type=int)
        reloadname = request.args.get('reloadname')
        if reloadname:
            data_list = apscheduler_tasklog.query.filter(apscheduler_tasklog.task_id.contains(reloadname)).all()
        else:
            data_list = apscheduler_tasklog.query.all()
        start=(page-1)*per_page
        end=page * per_page if len(data_list) > page * per_page else len(data_list)
        page_data=[data_list[i] for i in range(start,end)]
        data={"code":'0',"count":len(data_list),"data":to_json(page_data)}
        return data
    else:
        return render_template('admin_cronlog.html')


# 查看操作
@blue_cronlog.route("/admin_cronlogaction",methods=['GET','POST'])
@is_login
def admin_cronlogaction():
    dataid=request.values.get('dataid')
    if dataid:    #根据ID查出相关信息，防止用户提交修改过的POST信息。
        data_info=apscheduler_tasklog.query.filter_by(id=dataid).first()
        return render_template("admin_cronlogaction.html", data_info=data_info)
    else:          # 新增，不需要传参数。
        return render_template("admin_cronlogaction.html")
