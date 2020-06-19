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
用例名称: 维护故障时，切换为运营状态，操作失败
前置步骤：所有docker均已启动，roscore已运行。已屏蔽所有影响状态机的告警，状态机状态为维护锁车。
测试步骤：1、注入platform_datacollect_ultrasound故障ID 65540
          //上位机进入故障态，下位机进入故障态，告警ultrasound collection failed正确
          2、模拟pad下发切换运营模式
          //操作失败，5s内状态机仍为维护故障态
作者:Li Siying
创建时间：2019-08-09
'''

# 测试数据
ip = '0.0.0.0'

# 测试步骤
def State_change013():
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

    logging.info('1、注入platform_datacollect_ultrasound故障ID 65540'
                 '//上位机进入故障态，下位机进入故障态，告警ultrasound collect failed正确')
    fault_inject_pub(container,65540,1)

    # 上位机20s内进入维护故障
    for i in range(10):
        if state_machine_state_echo(container) != 3:
            time.sleep(2)
        else:
            break
        if i == 9:
            raise Exception('上位机未进入故障态')

    # 下位机进入故障
    state_machine = chassis_state_change_echo(container)
    if state_machine != 4:
        raise Exception('状态机预期为故障，实际为%d' %state_machine)

    # 查看产生对应告警
    alarm_info = communication_alarm_echo(container)
    if alarm_info['content'] != 'ultrasound collect failed' or alarm_info['type'] != '0':
        raise Exception('告警不正确')

    logging.info('2、模拟pad下发切换运营模式'
                 '//操作失败，5s内状态机仍为维护故障态')
    communication_control_pub(container, mode='vehicle_mode', state='operation')

    # 等待5s
    time.sleep(5)

    # 上位机为维护空闲态
    if state_machine_state_echo(container) != 3:
        raise Exception('当前状态不为维护故障')

    # 恢复故障
    fault_inject_pub(container,65540,0)

    # 查看告警取消的信息
    alarm_info = communication_alarm_echo(container)
    if alarm_info['content'] != 'ultrasound collect failed' or alarm_info['type'] != '1':
        raise Exception('告警不正确')

    # 上位机恢复维护锁车态
    if state_machine_state_echo(container) != 0:
        raise Exception('当前状态不为维护锁车')















