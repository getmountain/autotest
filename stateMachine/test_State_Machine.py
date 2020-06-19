# -*- coding:utf-8 -*-
import logging,time,os
from stateMachine.maintainState.State_change001 import State_change001
from stateMachine.maintainState.State_change002 import State_change002
from stateMachine.maintainState.State_change003 import State_change003
from stateMachine.maintainState.State_change004 import State_change004
from stateMachine.maintainState.State_change005 import State_change005
from stateMachine.maintainState.State_change006 import State_change006
# from State_change007 import State_change007
# from State_change008 import State_change008
# from State_change009 import State_change009
# from State_change010 import State_change010

import pytest
from Lib.Platform.Alarm import alarm_command,alarm_mask,self_check_service
from Lib.Platform.State_Machine import communication_control_pub
from Lib.Platform.fault_inject import fault_inject_pub
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
    fault_inject_pub(container,65541,0)
    fault_inject_pub(container,65537,0)
    # 进入锁车态
    communication_control_pub(container, mode='vehicle_state', state='lock')

def test_State_change001():
    State_change001()

def test_State_change002():
    State_change002()

def test_State_change003():
    State_change003()

def test_State_change004():
    State_change004()

def test_State_change005():
    State_change005()

def test_State_change006():
    State_change006()

# def test_State_change007():
#     State_change007()
#
# def test_State_change008():
#     State_change008()
#
# def test_State_change009():
#     State_change009()
#
# def test_State_change010():
#     State_change010()

if __name__ == "__main__":
    TestSuite =  os.path.basename(__file__)
    pytest.main(['-v',"--html=/home/nvidia/work/data/auto_result/report/" + ReportName,TestSuite])
