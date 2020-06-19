# coding:utf-8
import TX2
import logging
from Command.Container import Chassis
from Case_docker.lib.Chassis.Stata_Machine import chassis_control_state_pub,chassis_state_change_echo

'''
用例名称: 下位机状态机锁车，下发上锁，停车，手动，自动，故障恢复命令
前置步骤：所有docker除上位机状态机外均已启动。roscore已运行
测试步骤：1、查看当前状态为锁车
          //显示正确，为0
          2、下发上锁命令，停车，手动，自动，故障恢复命令
          //显示正确，为0
作者:Li Siying
创建时间：2019-05-13
'''
class Test_State_change009():
    def setup_method(self):
        self.ip = '0.0.0.0'
        tx2 = TX2.TX2(self.ip)
        self.containers = tx2.Containers()
        self.container = tx2.Containers()['chassis_serial']
    def teardown_method(self):
        chassis_control_state_pub(self.container, 'fault_rec')
        chassis_control_state_pub(self.container, 'stop')
        chassis_control_state_pub(self.container, 'lock')
    def test_State_change009(self):
        logging.info('1、查看当前状态为锁车'
                     '//显示正确，为0')
        state_machine = chassis_state_change_echo(self.container)
        if state_machine != 0:
            raise Exception('状态机初始状态不为锁车，实际为%d' %state_machine)

        logging.info('2、下发上锁命令，停车，手动，自动，故障恢复命令'
                     '//显示正确，为0')
        chassis_control_state_pub(self.container, 'lock')

        state_machine = chassis_state_change_echo(self.container)
        if state_machine != 0:
            raise Exception('状态机预期为落锁，实际为%d' %state_machine)

        chassis_control_state_pub(self.container, 'stop')

        state_machine = chassis_state_change_echo(self.container)
        if state_machine != 0:
            raise Exception('状态机预期为落锁，实际为%d' %state_machine)

        chassis_control_state_pub(self.container, 'manual')

        state_machine = chassis_state_change_echo(self.container)
        if state_machine != 0:
            raise Exception('状态机预期为落锁，实际为%d' %state_machine)

        chassis_control_state_pub(self.container, 'auto')

        state_machine = chassis_state_change_echo(self.container)
        if state_machine != 0:
            raise Exception('状态机预期为落锁，实际为%d' %state_machine)

        chassis_control_state_pub(self.container, 'fault_rec')

        state_machine = chassis_state_change_echo(self.container)
        if state_machine != 0:
            raise Exception('状态机预期为落锁，实际为%d' %state_machine)












