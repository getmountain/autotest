# coding:utf-8
import TX2
import logging
from Lib.Container import Exec_Run
from Lib.Chassis.fault_inject import tp_main_set,chassis_alarm_echo
from Lib.Chassis.Chassis_State import chassis_state_echo
'''
用例名称: 注入系统cpu温度高TP点，上报告警正确
前置步骤：所有docker均已启动。roscore已运行
测试步骤：1、注入系统cpu温度高TP点，查看告警
          //产生cpu异常告警system_alarm为131072
          2、取消TP点
          //告警恢复system_alarm为0
作者:Li Siying
创建时间：2019-08-13
'''

class Test_eTP_059():
    def setup_method(self):
        logging.info('---------before----------')
        self.ip = '0.0.0.0'
        tx2 = TX2.TX2(self.ip)
        self.containers = tx2.Containers()
        self.container = tx2.Containers()['chassis_serial']
    def teardown_method(self):
        logging.info('---------after-----------')
        tp_main_set(self.container, '59', '0')
    # 测试步骤
    def test_eTP_059(self):
        logging.info('1、注入系统cpu温度高TP点'
                     '//产生异常告警system_alarm为256')
        # 检查告警为bit17
        tp_main_set(self.container,'59','1')
        result = chassis_alarm_echo(self.container)
        if result['system_alarm'] != '131072':
            raise Exception('告警不正确')

        logging.info('2、取消TP点'
                     '//告警恢复system_alarm为0')
        # 检查告警恢复
        tp_main_set(self.container,'59','0')
        result = chassis_alarm_echo(self.container)
        if result['system_alarm'] != '0':
            raise Exception('告警未恢复')















