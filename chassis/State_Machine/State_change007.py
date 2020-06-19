# coding:utf-8
import TX2
import logging
from Command.Container import Chassis
from Case_docker.lib.Chassis.Stata_Machine import chassis_control_state_pub,chassis_state_change_echo

'''
用例名称: 下位机状态机手动驾驶切故障
前置步骤：所有docker除上位机状态机外均已启动。roscore已运行
测试步骤：1、查看当前状态为锁车
          //显示正确，为0
          2、下发解锁命令
          //显示正确，为1
          3、手动命令3
          //状态为2
          4、故障命令5
          //状态为4 
                
作者:Li Siying
创建时间：2019-05-12
'''
class Test_State_change007():
    def setup_method(self):
        self.ip = '0.0.0.0'
        tx2 = TX2.TX2(self.ip)
        self.containers = tx2.Containers()
        self.container = tx2.Containers()['chassis_serial']
    def teardown_method(self):
        chassis_control_state_pub(self.container, 'fault_rec')
        chassis_control_state_pub(self.container, 'stop')
        chassis_control_state_pub(self.container, 'lock')
    def test_State_change007(self):
        logging.info('1、查看当前状态为锁车'
                     '//显示正确，为0')
        state_machine = chassis_state_change_echo(self.container)
        if state_machine != 0:
            raise Exception('状态机初始状态不为运营故障，实际为%d' %state_machine)

        logging.info('2、下发解锁'
                     '//显示正确，为1')
        chassis_control_state_pub(self.container, 'unlock')

        state_machine = chassis_state_change_echo(self.container)
        if state_machine != 1:
            raise Exception('状态机预期为运营落锁，实际为%d' %state_machine)

        logging.info('3、下发手动驾驶'
                     '//显示正确，为2')
        chassis_control_state_pub(self.container, 'manual')

        state_machine = chassis_state_change_echo(self.container)
        if state_machine != 2:
            raise Exception('状态机预期为手动驾驶，实际为%d' %state_machine)

        logging.info('4、下发故障'
                     '//显示正确，为4')
        chassis_control_state_pub(self.container, 'fault')

        state_machine = chassis_state_change_echo(self.container)
        if state_machine != 4:
            raise Exception('状态机预期为故障，实际为%d' %state_machine)

        # 恢复
        chassis_control_state_pub(self.container, 'fault_rec')

        state_machine = chassis_state_change_echo(self.container)
        if state_machine != 0:
            raise Exception('状态机预期为运营落锁，实际为%d' %state_machine)














