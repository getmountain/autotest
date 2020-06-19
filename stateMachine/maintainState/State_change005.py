# coding:utf-8
import TX2
import logging
from Lib.Container import Exec_Run
from Lib.Platform.Alarm import self_check_service,communication_alarm_echo
from Lib.Platform.State_Machine import state_machine_state_echo,communication_control_pub
from Lib.Chassis.Stata_Machine import chassis_state_change_echo
from Lib.Platform.fault_inject import fault_inject_pub
'''
用例名称: 维护空闲时锁车，进入维护锁车
前置步骤：所有docker均已启动，roscore已运行。已屏蔽所有影响状态机的告警，状态机状态为维护锁车。
测试步骤：1、下发解锁命令
          //状态机切换为维护空闲
          2、下发上锁命令
          //状态机切换为维护锁车
          
作者:Li Siying
创建时间：2019-08-07
'''

# 测试数据
ip = '0.0.0.0'

# 测试步骤
def State_change005():
    logging.info('前置步骤：所有docker均已启动。roscore已运行。已屏蔽所有影响状态机的告警，状态机状态为维护锁车。')
    tx2 = TX2.TX2(ip)
    containers = tx2.Containers()
    container = tx2.Containers()['chassis_serial']
    tx2.Images()
    if len(containers) != 11:
        raise Exception('docker未全部启动')
    if not Exec_Run.Exec(container).roscore_check():
        raise Exception('roscore未自动启动')

    # 影响状态机告警为空
    if self_check_service(container):
        raise Exception('存在影响状态机的告警')

    # 查看上位机状态机状态
    if state_machine_state_echo(container) != 0:
        raise Exception('当前状态不为维护锁车')

    logging.info('1、下发解锁命令）'
                 '//状态机切换为维护空闲')
    communication_control_pub(container, mode='vehicle_state', state='unlock')

    # 查看状态机状态为维护空闲
    if state_machine_state_echo(container) != 1:
        raise Exception('当前状态不为维护空闲')

    logging.info('2、下发上锁命令）'
                 '//状态机切换为维护锁车')
    communication_control_pub(container, mode='vehicle_state', state='lock')

    # 查看状态机状态为维护空闲
    if state_machine_state_echo(container) != 0:
        raise Exception('当前状态不为维护锁车')






























