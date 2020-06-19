# -*- coding:utf-8 -*-
import logging,time,os
from State_change011 import State_change011
from State_change012 import State_change012
from State_change013 import State_change013
from State_change014 import State_change014
from State_change015 import State_change015
from State_change016 import State_change016
from State_change017 import State_change017
from State_change018 import State_change018
from State_change019 import State_change019
from State_change020 import State_change020
import pytest
from Case_docker.lib.Platform.Alarm import alarm_command,alarm_mask,self_check_service
from Case_docker.lib.Platform.State_Machine import communication_control_pub
from Case_docker.lib.Platform.fault_inject import fault_inject_pub
import TX2

# 测试数据
ip = '0.0.0.0'
RunTime = time.strftime("%Y-%m-%d %H-%M-%S", time.localtime())
ReportName = RunTime + '.html'
LogName = RunTime + '.log'

logging.basicConfig(level=logging.INFO,filename='/home/nvidia/work/data/auto_result/log/' + LogName,
                    format='%(levelname)s: %(message)s- %(filename)s[line:%(lineno)d]-%(asctime)s')

logging.info('前置步骤：所有docker除上位机状态机外均已启动。roscore已运行')
tx2 = TX2.TX2(ip)
containers = tx2.Containers()
container = tx2.Containers()['chassis_serial']
# 获取已有的所有告警
id_list = self_check_service(container)

def setup_module():
    # 屏蔽已有告警
    if id_list:
        for alarm_id in id_list:
            alarm_mask(container, int(alarm_id))
        for alarm_id in id_list:
            alarm_command(container,id=int(alarm_id),mask_state='false',check_mask='false')

def teardown_module():
    pass

def setup_function():
    pass

def teardown_function():
    # 取消故障注入
    fault_inject_pub(container,65540,0)
    fault_inject_pub(container,65537,0)
    fault_inject_pub(container,65538,0)
    fault_inject_pub(container,16842753,0)
    # 进入维护锁车态
    communication_control_pub(container, mode='vehicle_state', state='ready')
    communication_control_pub(container, mode='vehicle_state', state='lock')
    communication_control_pub(container, mode='vehicle_mode', state='maintenance')

def test_State_change011():
    State_change011()

def test_State_change012():
    State_change012()

def test_State_change013():
    State_change013()

def test_State_change014():
    State_change014()

def test_State_change015():
    State_change015()

def test_State_change016():
    State_change016()

def test_State_change017():
    State_change017()

def test_State_change018():
    State_change018()

def test_State_change019():
    State_change019()

def test_State_change020():
    State_change020()

if __name__ == "__main__":
    TestSuite =  os.path.basename(__file__)
    pytest.main(["--html=/home/nvidia/work/data/auto_result/report/" + ReportName,TestSuite])