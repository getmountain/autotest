# test_State_Machine.py
# coding:utf-8
import logging,time,os
from State_change001 import Test_State_change001
from State_change002 import Test_State_change002
from State_change003 import Test_State_change003
from State_change004 import Test_State_change004
from State_change005 import Test_State_change005
from State_change006 import Test_State_change006
from State_change007 import Test_State_change007
from State_change008 import Test_State_change008
from State_change009 import Test_State_change009
from State_change010 import Test_State_change010
from State_change011 import Test_State_change011
from State_change012 import Test_State_change012
import pytest_html
import pytest
from Case_docker.lib.Chassis.log_sd import collect_log,init_collect_log
import TX2

logging.basicConfig(level=logging.INFO,
                    format='%(levelname)s: %(message)s- %(filename)s[line:%(lineno)d]-%(asctime)s')
# 测试数据
ip = '0.0.0.0'
path = os.getcwd().replace('/autotest/','/auto_result/log/') + '/'
RunTime = time.strftime("%Y-%m-%d %H-%M-%S", time.localtime())
ReportName = RunTime + '.html'
LogName = RunTime + '.log'
TestSuite = os.path.basename(__file__)
logpath = path + TestSuite.split('.')[0] + time.strftime("_%Y-%m-%d_%H-%M-%S.log", time.localtime())

tx2 = TX2.TX2(ip)
containers = tx2.Containers()
container = tx2.Containers()['chassis_serial']
StateMacine_con = tx2.Containers()['state_machine']

def setup_module():
    # 清除日志
    init_collect_log(container, logpath)
    StateMacine_con.stop()

def teardown_module():
    os.system('docker start state_machine')
    StateMacine_con.start()
    collect_log(container,logpath=logpath)

Test_State_change001()
Test_State_change002()
Test_State_change003()
Test_State_change004()
Test_State_change005()
Test_State_change006()
Test_State_change007()
Test_State_change008()
Test_State_change009()
Test_State_change010()
Test_State_change011()
Test_State_change012()

if __name__ == "__main__":
    pytest.main(['-x',"--html=/home/nvidia/work/data/auto_result/report/" + ReportName,TestSuite])