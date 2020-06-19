# -*- coding:UTF-8 -*-
import time
import os,sys
from eTP_040 import Test_eTP_040
from eTP_041 import Test_eTP_041
from eTP_042 import Test_eTP_042
from eTP_043 import Test_eTP_043
from eTP_044 import Test_eTP_044
from eTP_045 import Test_eTP_045
from eTP_046 import Test_eTP_046
from eTP_047 import Test_eTP_047
from eTP_048 import Test_eTP_048
from eTP_049 import Test_eTP_049
import pytest
import TX2
import logging
from Case_docker.lib.Chassis.log_sd import collect_log,init_collect_log
from Case_docker.lib.Chassis.fault_inject import tp_main_set,chassis_alarm_echo
from Command.Container import Chassis


# 测试数据
ip = '0.0.0.0'
path = os.getcwd().replace('/autotest/','/auto_result/log/') + '/'
RunTime = time.strftime("%Y-%m-%d %H-%M-%S", time.localtime())
ReportName = RunTime + '.html'
LogName = RunTime + '.log'
TestSuite = os.path.basename(__file__)
logpath = path + TestSuite.split('.')[0] + time.strftime("_%Y-%m-%d_%H-%M-%S.log", time.localtime())

logging.basicConfig(level=logging.INFO,
                   format='%(levelname)s: %(message)s- %(filename)s[line:%(lineno)d]-%(asctime)s')

logging.info('前置步骤：所有docker均已启动。roscore已运行')
tx2 = TX2.TX2(ip)
containers = tx2.Containers()
container = tx2.Containers()['chassis_serial']
if len(containers) != 11:
    raise Exception('docker未全部启动')
if not Chassis.Exec(container).roscore_check():
    raise Exception('roscore未自动启动')

def setup_module():
    # 清除日志
    init_collect_log(container, logpath)
    # 检查是否无告警
    result = chassis_alarm_echo(container)
    for key in result.keys():
        if 'alarm' in key and result[key] != '0':
            raise Exception('存在异常告警')

def teardown_module():
    # 恢复，停车落锁
    collect_log(container,logpath=logpath)

Test_eTP_040()
Test_eTP_041()
Test_eTP_042()
Test_eTP_043()
Test_eTP_044()
Test_eTP_045()
Test_eTP_046()
Test_eTP_047()
Test_eTP_048()
Test_eTP_049()

if __name__ == "__main__":
    pytest.main(['-x',"--html=/home/nvidia/work/data/auto_result/report/" + ReportName,TestSuite])