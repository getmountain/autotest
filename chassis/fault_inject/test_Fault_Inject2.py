# -*- coding:UTF-8 -*-
import time
import os,sys
from eTP_010 import Test_eTP_010
from eTP_011 import Test_eTP_011
from eTP_012 import Test_eTP_012
from eTP_013 import Test_eTP_013
from eTP_017 import Test_eTP_017
from eTP_018 import Test_eTP_018
from eTP_019 import Test_eTP_019
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

Test_eTP_010()
Test_eTP_011()
Test_eTP_012()
Test_eTP_013()
Test_eTP_017()
Test_eTP_018()
Test_eTP_019()

if __name__ == "__main__":
    pytest.main(['-x',"--html=/home/nvidia/work/data/auto_result/report/" + ReportName,TestSuite])