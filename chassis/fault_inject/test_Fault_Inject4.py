# -*- coding:UTF-8 -*-
import time
import os,sys
from eTP_030 import Test_eTP_030
from eTP_031 import Test_eTP_031
from eTP_032 import Test_eTP_032
from eTP_033 import Test_eTP_033
from eTP_034 import Test_eTP_034
from eTP_035 import Test_eTP_035
from eTP_036 import Test_eTP_036
from eTP_037 import Test_eTP_037
from eTP_038 import Test_eTP_038
from eTP_039 import Test_eTP_039
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

Test_eTP_030()
Test_eTP_031()
Test_eTP_032()
Test_eTP_033()
Test_eTP_034()
Test_eTP_035()
Test_eTP_036()
Test_eTP_037()
Test_eTP_038()
Test_eTP_039()

if __name__ == "__main__":
    pytest.main(['-x',"--html=/home/nvidia/work/data/auto_result/report/" + ReportName,TestSuite])