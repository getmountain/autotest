# coding:utf-8
import TX2
import logging
from Lib.Container import Exec_Run
from Lib.Chassis.fault_inject import tp_main_set,chassis_alarm_echo
from Lib.Chassis.Chassis_State import chassis_state_echo
'''
用例名称: 注入系统cpu温度超高TP点，上报告警正确
前置步骤：所有docker均已启动。roscore已运行
测试步骤：1、注入系统cpu温度超高TP点，查看告警
          //产生cpu异常告警system_alarm为262144
          2、取消TP点
          //告警恢复system_alarm为0
作者:Li Siying
创建时间：2019-08-13
'''

class Test_eTP_060():
    def setup_method(self):
        logging.info('---------before----------')
        self.ip = '0.0.0.0'
        tx2 = TX2.TX2(self.ip)
        self.containers = tx2.Containers()
        self.container = tx2.Containers()['chassis_serial']
    def teardown_method(self):
        logging.info('---------after-----------')
        tp_main_set(self.container, '60', '0')
    # 测试步骤
    def test_eTP_060(self):
        logging.info('1、注入系统cpu温度超高TP点'
                     '//产生异常告警system_alarm为262144')
        # 检查告警为bit18
        tp_main_set(self.container,'60','1')
        result = chassis_alarm_echo(self.container)
        if result['system_alarm'] != '262144':
            raise Exception('告警不正确')

        logging.info('2、取消TP点'
                     '//告警恢复system_alarm为0')
        # 检查告警恢复
        tp_main_set(self.container,'60','0')
        result = chassis_alarm_echo(self.container)
        if result['system_alarm'] != '0':
            raise Exception('告警未恢复')















