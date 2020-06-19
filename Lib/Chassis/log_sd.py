# coding:utf-8
import re
import time
from Command.Container import Chassis
import os



def log_sd_clean(container):
    '''
    通过/chassis/cmd_req对日志进行[<clean>]操作，例如：
    rostopic pub -1 /chassis/cmd_req std_msgs/String "data: 'log_sd clean'"
    '''
    data_value = "log_sd clean"
    data = '"data: %s"' % data_value
    Chassis.Exec(container).rostopic_pub(topic='/chassis/cmd_req',msg_type='std_msgs/String ',args=data)

def log_sd_flush(container):
    '''
    通过/chassis/cmd_req对日志进行[<flush>]操作，例如：
    rostopic pub -1 /chassis/cmd_req std_msgs/String "data: 'log_sd flush'"
    '''
    data_value = "log_sd clean"
    data = '"data: %s"' % data_value
    Chassis.Exec(container).rostopic_pub(topic='/chassis/cmd_req',msg_type='std_msgs/String ',args=data)

def log_sd_read(container,logpath):
    '''
    以调用/opt/routineCar/log/auto_scripts下的脚本的方式，
    通过/chassis/cmd_req对日志进行[<read>]操作，并将读取结果存放到logpath，例如：
    rostopic pub -1 /chassis/cmd_req std_msgs/String "data: 'log_sd read'"
    '''
    script = '/opt/routineCar/log/auto_scripts/log_read.sh'
    if not os.path.isfile(script):
        os.mkdir('/opt/routineCar/log/auto_scripts')
        os.system('cp /home/nvidia/work/data/autotest/Script/log_read.sh %s'%script)
    logdir = logpath.split('test_')[0]
    if not os.path.isdir(logdir):
        os.system('mkdir -p %s'%logdir)
    RunTime = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
    logname = logpath+'_'+RunTime+'.log'
    #cmd = "bash %s" %script

    container.exec_run('bash %s %s' %(script,logname))

def init_collect_log(container,logpath):
    data = r'''"data: '{\"message_id\":123441,\"from\":\"communication\",\"to\":\"control\",\"log_collect\":{
    \"collect_target\": \"vehicle\",\"jwt\": \"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE4NzYyODI5NzIsImp0aSI6ImJkNWNkMGI1MDhlYTA4ZWUiLCJpYXQiOjE1NjA5MjI5NzJ9.1HSPUz2fE58fxPRBaxx4AhPdmTgZWtAvMyd6SvLcQeY\",
    \"upload_status\": \"22\",\"access_key\": \"AKIAO2DNISXSC7YGDAQA--\",\"secret_key\": \"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\",\"token\": \"XXX\",\"reply_url\": \"https://dev-logcull.goldenridge.cn/log-collect/v1/tx2UploadReply--\",
    \"start_time\": \"2019-5-1\",\"end_time\": \"2019-8-1\",\"vehicle_log_type\": \"log\",\"software_attribute\": \"all\",
    \"collect_num\": \"2\",\"module\": [\"chassis\"]}}'"'''
    File = os.path.join('/opt/routineCar/log/chassis',time.strftime('%Y-%m-%d',time.localtime()) + '.txt')
    os.system('rm -rf %s'%File)
    stop_ftp_task(container)
    Chassis.Exec(container).rostopic_pub(topic='/communication/control',msg_type='std_msgs/String ',args=data)
    for i in range(10):
        if os.path.isfile(File):
            break
        else:
            time.sleep(3)
        if i == 9:
            raise Exception('采集日志失败')
    logdir = logpath.split('test_')[0]
    if not os.path.isdir(logdir):
        os.system('mkdir -p %s' % logdir)
        time.sleep(2)
    #os.system('mv '+ File + ' ' + logpath)
    os.system('cp %s %s'%(File,logpath))
    time.sleep(2)
    return logpath

def collect_log(container,logpath):
    data = r'''"data: '{\"message_id\":123441,\"from\":\"communication\",\"to\":\"control\",\"log_collect\":{
    \"collect_target\": \"vehicle\",\"jwt\": \"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE4NzYyODI5NzIsImp0aSI6ImJkNWNkMGI1MDhlYTA4ZWUiLCJpYXQiOjE1NjA5MjI5NzJ9.1HSPUz2fE58fxPRBaxx4AhPdmTgZWtAvMyd6SvLcQeY\",
    \"upload_status\": \"22\",\"access_key\": \"AKIAO2DNISXSC7YGDAQA--\",\"secret_key\": \"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\",\"token\": \"XXX\",\"reply_url\": \"https://dev-logcull.goldenridge.cn/log-collect/v1/tx2UploadReply--\",
    \"start_time\": \"2019-5-1\",\"end_time\": \"2019-8-1\",\"vehicle_log_type\": \"log\",\"software_attribute\": \"all\",
    \"collect_num\": \"2\",\"module\": [\"chassis\"]}}'"'''
    File = os.path.join('/opt/routineCar/log/chassis',time.strftime('%Y-%m-%d',time.localtime()) + '.txt')
    os.system('rm -rf %s'%File)
    stop_ftp_task(container)
    Chassis.Exec(container).rostopic_pub(topic='/communication/control',msg_type='std_msgs/String ',args=data)
    for i in range(10):
        if os.path.isfile(File):
            break
        else:
            time.sleep(3)
        if i == 9:
            raise Exception('采集日志失败')
    if not os.path.isfile(logpath):
        raise Exception('初始日志不存在')
    os.system('grep -xvFf %s %s | tee %s' %(logpath,File,logpath))
    time.sleep(2)
    return logpath

def stop_ftp_task(container):
    data = r'''"data: '{\"message_id\":123441,\"from\":\"communication\",\"to\":\"control\",\"log_collect\":{
    \"collect_target\": \"vehicle\",\"jwt\": \"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE4NzYyODI5NzIsImp0aSI6ImJkNWNkMGI1MDhlYTA4ZWUiLCJpYXQiOjE1NjA5MjI5NzJ9.1HSPUz2fE58fxPRBaxx4AhPdmTgZWtAvMyd6SvLcQeY\",
    \"upload_status\": \"stop\",\"access_key\": \"AKIAO2DNISXSC7YGDAQA--\",\"secret_key\": \"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\",\"token\": \"XXX\",\"reply_url\": \"https://dev-logcull.goldenridge.cn/log-collect/v1/tx2UploadReply--\",
    \"start_time\": \"2019-5-1\",\"end_time\": \"2019-8-1\",\"vehicle_log_type\": \"log\",\"software_attribute\": \"all\",
    \"collect_num\": \"2\",\"module\": [\"chassis\"]}}'"'''
    Chassis.Exec(container).rostopic_pub(topic='/communication/control',msg_type='std_msgs/String ',args=data)