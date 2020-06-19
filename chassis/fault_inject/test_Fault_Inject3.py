# -*- coding:UTF-8 -*-
import time
import os,sys
from eTP_020 import Test_eTP_020
from eTP_021 import Test_eTP_021
from eTP_022 import Test_eTP_022
from eTP_023 import Test_eTP_023
from eTP_024 import Test_eTP_024
from eTP_025 import Test_eTP_025
from eTP_026 import Test_eTP_026
from eTP_027 import Test_eTP_027
from eTP_028 import Test_eTP_028
from eTP_029 import Test_eTP_029
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

Test_eTP_020()
Test_eTP_021()
Test_eTP_022()
Test_eTP_023()
Test_eTP_024()
Test_eTP_025()
Test_eTP_026()
Test_eTP_027()
Test_eTP_028()
Test_eTP_029()

if __name__ == "__main__":
    pytest.main(['-x',"--html=/home/nvidia/work/data/auto_result/report/" + ReportName,TestSuite])