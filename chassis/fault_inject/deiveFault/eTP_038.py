# coding:utf-8
import TX2
import logging
from Lib.Container import Exec_Run
from Lib.Chassis.fault_inject import tp_main_set,chassis_alarm_echo
from Lib.Chassis.Chassis_State import chassis_state_echo
'''
用例名称: 注入右驱动器短路TP点，产生故障后恢复
前置步骤：所有docker均已启动。roscore已运行
测试步骤：1、注入右驱动器短路TP点
          //产生正确告警，motor_driver_alarm为2048（bit11）
          2、取消TP点
          //告警恢复，motor_driver_alarm为0   
作者:Li Siying
创建时间：2019-06-28
'''

class Test_eTP_038():
    def setup_method(self):
        logging.info('---------before----------')
        self.ip = '0.0.0.0'
        tx2 = TX2.TX2(self.ip)
        self.containers = tx2.Containers()
        self.container = tx2.Containers()['chassis_serial']
    def teardown_method(self):
        logging.info('---------after-----------')
        tp_main_set(self.container, '38', '0')
    # 测试步骤
    def test_eTP_038(self):
        logging.info('1、注入右驱动器短路TP点'
                     '//产生正确告警，motor_driver_alarm为2048')
        tp_main_set(self.container,'38','1')
        result = chassis_alarm_echo(self.container)
        if result['motor_driver_alarm'] != '2048':
            raise Exception('告警不正确')

        logging.info('2、取消TP点'
                     '//告警恢复，motor_driver_alarm为0')
        tp_main_set(self.container,'38','0')
        result = chassis_alarm_echo(self.container)
        if result['motor_driver_alarm'] != '0':
            raise Exception('告警未恢复')











