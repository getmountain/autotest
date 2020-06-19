# coding:utf-8
import TX2
import logging
from Lib.Container import Exec_Run
from Lib.Platform.Alarm import self_check_service,communication_alarm_echo
from Lib.Platform.State_Machine import state_machine_state_echo,communication_control_pub
from Lib.Chassis.Stata_Machine import chassis_state_change_echo
from Lib.Platform.fault_inject import fault_inject_pub
import time
'''
用例名称: 维护锁车时发生不可自动驾驶故障，不处理
前置步骤：所有docker均已启动，roscore已运行。已屏蔽所有影响状态机的告警，状态机状态为维护锁车。
测试步骤：1、注入不可自动驾驶故障（数据采集错误，故障ID 65537）
          //状态机状态10秒内不改变
作者:Li Siying
创建时间：2019-08-07
'''

# 测试数据
ip = '0.0.0.0'

# 测试步骤
def State_change003():
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

    logging.info('1、注入不可自动驾驶故障（数据采集错误，故障ID 65537）'
                 '//状态机状态10秒内不改变')
    # 注入platform_datacollect_odom故障,id 65537
    fault_inject_pub(container,65537,1)

    # 20s内查看产生对应告警
    for i in range(5):
        alarm_info = communication_alarm_echo(container)
        if alarm_info['content'] != 'odom collect failed' or alarm_info['type'] != '0':
            time.sleep(5)
        else:
            break
        if i == 4:
            raise Exception('未产生对应告警')

    # 上位机仍为维护锁车态
    if state_machine_state_echo(container) != 0:
        raise Exception('当前状态不为维护锁车')

    # 下位机为锁车态
    state_machine = chassis_state_change_echo(container)
    if state_machine != 0:
        raise Exception('状态机预期为锁车，实际为%d' %state_machine)

    # 取消故障注入
    fault_inject_pub(container,65537,0)

    # 查看告警取消的信息
    alarm_info = communication_alarm_echo(container)
    if alarm_info['content'] != 'odom collect failed' or alarm_info['type'] != '1':
        raise Exception('告警不正确')









