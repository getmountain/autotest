# -*- coding:UTF-8 -*-
import time
import os,sys
from eTP_050 import Test_eTP_050
from eTP_051 import Test_eTP_051
from eTP_052 import Test_eTP_052
from eTP_053 import Test_eTP_053
from eTP_054 import Test_eTP_054
from eTP_055 import Test_eTP_055
from eTP_056 import Test_eTP_056
from eTP_057 import Test_eTP_057
from eTP_058 import Test_eTP_058
from eTP_059 import Test_eTP_059
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

Test_eTP_050()
Test_eTP_051()
Test_eTP_052()
Test_eTP_053()
Test_eTP_054()
Test_eTP_055()
Test_eTP_056()
Test_eTP_057()
Test_eTP_058()
Test_eTP_059()

if __name__ == "__main__":
    pytest.main(['-x',"--html=/home/nvidia/work/data/auto_result/report/" + ReportName,TestSuite])