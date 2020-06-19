# -*- coding:utf-8 -*-
import logging,time,os

from State_change021 import State_change021
from State_change022 import State_change022
from State_change023 import State_change023
from State_change024 import State_change024
from State_change025 import State_change025
from State_change026 import State_change026
from State_change027 import State_change027
from State_change028 import State_change028
from State_change029 import State_change029
from State_change030 import State_change030
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
    fault_inject_pub(container,65541,0)
    fault_inject_pub(container,65537,0)
    fault_inject_pub(container,65538,0)
    fault_inject_pub(container,16842753,0)
    # 进入维护锁车态
    communication_control_pub(container, mode='vehicle_state', state='ready')
    communication_control_pub(container, mode='vehicle_state', state='lock')
    communication_control_pub(container, mode='vehicle_mode', state='maintenance')

def test_State_change021():
    State_change021()

def test_State_change022():
    State_change022()

def test_State_change023():
    State_change023()

def test_State_change024():
    State_change024()

def test_State_change025():
    State_change025()

def test_State_change026():
    State_change026()

def test_State_change027():
    State_change027()

def test_State_change028():
    State_change028()

def test_State_change029():
    State_change029()

def test_State_change030():
    State_change030()

if __name__ == "__main__":
    TestSuite =  os.path.basename(__file__)
    pytest.main(["--html=/home/nvidia/work/data/auto_result/report/" + ReportName,TestSuite])
