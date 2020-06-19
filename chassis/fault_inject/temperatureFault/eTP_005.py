# coding:utf-8
import TX2
import logging
from Lib.Container import Exec_Run
from Lib.Chassis.fault_inject import tp_main_set,chassis_alarm_echo
from Lib.Chassis.Chassis_State import chassis_state_echo
'''
用例名称: 注入超低温TP点，产生故障后恢复
前置步骤：所有docker均已启动。roscore已运行
测试步骤：1、注入超低温TP点
          //产生正确告警，power_alarm为256
          2、取消TP点
          //告警恢复   
作者:Li Siying
创建时间：2019-06-25
'''

class Test_eTP_005():
    def setup_method(self):
        logging.info('---------before----------')
        self.ip = '0.0.0.0'
        tx2 = TX2.TX2(self.ip)
        self.containers = tx2.Containers()
        self.container = tx2.Containers()['chassis_serial']
    def teardown_method(self):
        logging.info('---------after-----------')
        tp_main_set(self.container, '5', '0')
    # 测试步骤
    def test_eTP_005(self):
        logging.info('1、注入超低温TP点'
                     '//产生正确告警，bit8超低温')
        tp_main_set(self.container,'5','1')
        result = chassis_alarm_echo(self.container)
        if result['power_alarm'] != '256':
            raise Exception('告警不正确')

        logging.info('2、取消TP点'
                     '//告警恢复')
        tp_main_set(self.container,'5','0')
        result = chassis_alarm_echo(self.container)
        if result['power_alarm'] != '0':
            raise Exception('告警未恢复')











