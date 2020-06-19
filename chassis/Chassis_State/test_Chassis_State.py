# -*- coding:UTF-8 -*-
import time
import os
import pytest
import TX2
import logging
from default_state import default_state


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

def setup_module():
    pass

def teardown_module():
    logging.info('---------恢复docker状态机-------------')

def setup_function():
    pass

def teardown_function():
    # 恢复，停车落锁
    logging.info('————清环境————')

def test_default_state():
    logging.info('case start')
    default_state()

if __name__ == "__main__":
    TestSuite =  os.path.basename(__file__)
    pytest.main(["--html=/home/nvidia/work/data/auto_result/report/" + ReportName,TestSuite])