#encoding:utf-8
import subprocess
from ..models import apscheduler_tasklog
from ..exts import db

# 执行CMD命令
def exe_cmd(cmd,task_id):
    status, output = subprocess.getstatusoutput(cmd)
    data = dict(
        task_id = task_id,
        task_status = True if status == 0 else False,
        task_cmd = cmd,
        task_stdout = output
    )
    tasklog_add = apscheduler_tasklog(**data)
    db.session.add(tasklog_add)
    db.session.commit()
    return output


def jobfromparm(scheduler,**jobargs):
    id = jobargs['id']
    func=__name__+':'+'exe_cmd'
    args = jobargs['cmd']
    cron = jobargs['cron'].split(' ')
    cron_rel = dict(second=cron[0], minute=cron[1], hour=cron[2], day=cron[3], month=cron[4], day_of_week=cron[5])
    #print('[add job]: ',id)
    scheduler.add_job(func=func,id=id, kwargs={'cmd':args,'task_id':id},trigger='cron',**cron_rel,replace_existing=True)
    #print('[add job ok]')
    return id



# 把cron结果转为列表
def job_tolist(data):
    data_list = []
    for ret in data:
        fields = ret.trigger.fields
        cron = {}
        for field in fields:
            cron[field.name] = str(field)
        cron_list = [cron['second'], cron['minute'], cron['hour'], cron['day'], cron['month'],
                     cron['day_of_week']]
        info = {
            'id': ret.id,
            'next_run_time': ret.next_run_time,
            'cmd': ret.kwargs.get('cmd'),
            # 'func':ret.func_ref,
            'status': 'running' if ret.next_run_time != None else 'stop',
            'cron': ' '.join(cron_list)
        }
        data_list.append(info)
    return data_list



