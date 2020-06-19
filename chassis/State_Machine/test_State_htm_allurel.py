# -*- coding:UTF-8 -*-
import time
import logging
import os
from State_change009 import State_change009
import pytest
from Case_docker.lib.Chassis.Stata_Machine import chassis_control_state_pub
import TX2

# site.getsitepackages()
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
StateMacine_con = tx2.Containers()['state_machine']

def setup_module():
    containers = tx2.Containers()
    logging.info(str(len(containers)))
    StateMacine_con.stop()
    chassis_control_state_pub(container,'fault_rec')
    containers = tx2.Containers()
    logging.info(str(len(containers)))

def teardown_module():
    logging.info('---------恢复docker状态机-------------')
    StateMacine_con.start()

def setup_function():
    pass

def teardown_function():
    # 恢复，停车落锁
    logging.info('————清环境————')
    chassis_control_state_pub(container,'fault_rec')
    chassis_control_state_pub(container,'stop')
    chassis_control_state_pub(container,'lock')

def test_state01():
    logging.info('case start')
    State_change009()

if __name__ == "__main__":
    TestSuite =  os.path.basename(__file__)
    pytest.main(["--alluredir=/home/nvidia/work/data/auto_result/report/" + ReportName,TestSuite])