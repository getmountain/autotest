# coding:utf-8
import TX2
import logging
from Lib.Container import Exec_Run
from Lib.Chassis.fault_inject import tp_main_set,chassis_alarm_echo
from Lib.Chassis.Chassis_State import chassis_state_echo
'''
用例名称: 注入TP点，使状态机任务剩余堆栈量达到告警值
前置步骤：所有docker均已启动。roscore已运行
测试步骤：1、注入10号TP点，模拟状态机任务剩余堆栈量为49
          //产生状态机堆栈异常告警system_alarm为8，下位机状态显示堆栈剩余量为49
          2、取消TP点
          //告警恢复system_alarm为0，且下位机状态堆栈剩余量不为49
作者:Li Siying
创建时间：2019-06-26
'''

class Test_eTP_010():
    def setup_method(self):
        logging.info('---------before----------')
        self.ip = '0.0.0.0'
        tx2 = TX2.TX2(self.ip)
        self.containers = tx2.Containers()
        self.container = tx2.Containers()['chassis_serial']
    def teardown_method(self):
        logging.info('---------after-----------')
        tp_main_set(self.container, '10', '0')
    # 测试步骤
    def test_eTP_010(self):
        logging.info('1、注入10号TP点，模拟状态机任务剩余堆栈量为49'
                     '//产生状态机堆栈异常告警system_alarm为8，下位机状态显示堆栈剩余量为49')
        # 检查告警为bit3
        tp_main_set(self.container,eTP_num='10',switch='1')
        result = chassis_alarm_echo(self.container)
        if result['system_alarm'] != '8':
            raise Exception('告警不正确')

        # 检查堆栈剩余量
        result = chassis_state_echo(self.container)
        if '[49,' not in result['stack_rec']:
            raise Exception('堆栈剩余量不为49')

        logging.info('2、取消TP点'
                     '//告警恢复system_alarm为0，且下位机状态堆栈剩余量不为49')
        # 检查告警恢复
        tp_main_set(self.container,'10','0')
        result = chassis_alarm_echo(self.container)
        if result['system_alarm'] != '0':
            raise Exception('告警未恢复')

        # 检查堆栈剩余量
        result = chassis_state_echo(self.container)
        if '[49,' in result['stack_rec']:
            raise Exception('堆栈剩余量未恢复')














