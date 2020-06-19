# coding:utf-8
import time
import TX2
import logging
from Lib.Container import Exec_Run
from Lib.Platform.Alarm import self_check_service,communication_alarm_echo
from Lib.Platform.State_Machine import state_machine_state_echo,communication_control_pub
from Lib.Chassis.Stata_Machine import chassis_state_change_echo
from Lib.Platform.fault_inject import fault_inject_pub
'''
用例名称: 维护锁车切换为运营锁车
前置步骤：所有docker均已启动，roscore已运行。已屏蔽所有影响状态机的告警，状态机状态为维护锁车。
测试步骤：1、切换运营模式
          //上位机进入锁车模式，下位机进入锁车态
作者:Li Siying
创建时间：2019-08-06
'''

# 测试数据
ip = '0.0.0.0'

# 测试步骤
def State_change002():
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

    logging.info('1、切换运营模式'
                 '//上位机进入运营锁车模式，下位机进入锁车态')

    communication_control_pub(container, mode='vehicle_mode', state='operation')

    # 上位机为运营锁车态
    if state_machine_state_echo(container) != 4:
        raise Exception('当前状态不为运营锁车')

    # 下位机进入锁车态
    state_machine = chassis_state_change_echo(container)
    if state_machine != 0:
        raise Exception('状态机预期为锁车，实际为%d' %state_machine)

    # 恢复为维护模式
    communication_control_pub(container, mode='vehicle_mode', state='maintenance')
    if state_machine_state_echo(container) != 0:
        raise Exception('当前状态不为维护锁车')










