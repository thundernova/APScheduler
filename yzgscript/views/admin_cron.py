from flask import Blueprint, request, render_template
from ..exts import scheduler
from ..public import is_login
from .scheduler_core import jobfromparm,job_tolist

blue_cron = Blueprint("blue_cron",__name__)



# 获取所有数据
@blue_cron.route("/admin_cron",methods=['GET'])
@is_login
def admin_cron():
    if request.args.get('action'):
        reloadname = request.args.get('reloadname')
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('limit', 10, type=int)
        ret_list = scheduler.get_jobs() if reloadname==None else [scheduler.get_job(reloadname)]
        try:
            data_list=job_tolist(ret_list)
            start=(page-1)*per_page
            end=page * per_page if len(data_list) > page * per_page else len(data_list)
            page_data=[data_list[i] for i in range(start,end)]
            response={"code":'0',"count":len(data_list),"data":page_data}
        except Exception as e:
            response={"code":1,"count":0,"data":str(e)}
        return response
    else:
        return render_template('admin_cron.html')



# 新增、修改操作
@blue_cron.route("/admin_cronaction",methods=['GET','POST'])
@is_login
def admin_cronaction():
    data=request.values
    if 'id' in data:
        old_data=scheduler.get_job(data['id'])
    if request.method == 'POST':
        try:
            if data['action']=='add' and old_data:
                print ("old_data",old_data)
                response = {"code": '201', "msg": "job[%s] already exists!" %data['id']}
            else:
                add_job = jobfromparm(scheduler, **data)
                response = {"code": '200', "msg": "job[%s] add success!" %add_job}
        except Exception as e:
            response = {"code": '500', "msg": str(e)}
        return response
    else:
        if data['action']=='edit':
            info=job_tolist([old_data])
            response = {'action': data['action'], 'info': info}
        else:
            response={'action':data['action']}
        return render_template("admin_cronaction.html",data=response)



# 启用、停用、删除操作
@blue_cron.route("/admin_cronop",methods=['GET','POST'])
@is_login
def admin_cronop():
    response = {'code': '500'}
    dataid=request.values.get('dataid').split(',')
    adminop=request.values.get('action')
    try:
        if adminop == 'del':
            for i in range(len(dataid)):
                scheduler.remove_job(dataid[i])
            response['msg'] = "job [%s] remove success!"%dataid
        elif adminop=='stop':
            scheduler.pause_job(dataid)
            response['msg'] = "job [%s] pause success!" %dataid
        else:
            scheduler.resume_job(dataid)
            response['msg'] = "job [%s] start success!" %dataid
        response['code'] = 200
    except Exception as e:
        response = {"code": '500', "msg": str(e)}
    return response