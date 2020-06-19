# coding:utf-8
import TX2
import logging
from Lib.Container import Exec_Run
from Lib.Platform.Alarm import self_check_service,communication_alarm_echo
from Lib.Platform.State_Machine import state_machine_state_echo,communication_control_pub
from Lib.Chassis.Stata_Machine import chassis_state_change_echo
from Lib.Platform.fault_inject import fault_inject_pub
'''
用例名称: 运营就绪时，发生不可使用故障，进入故障态
前置步骤：所有docker均已启动，roscore已运行。已屏蔽所有影响状态机的告警，状态机状态为维护锁车。
测试步骤：1、切换运营模式
          //上位机进入运营锁车模式
          2、下发解锁命令
          //上位机进入运营就绪态
          3、注入platform_datacollect_sensor_state故障,id65541
          //上位机状态机切换为运营故障，下位机状态机切换为故障态
          
作者:Li Siying
创建时间：2019-08-12
'''

# 测试数据
ip = '0.0.0.0'

# 测试步骤
def State_change023():
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
                 '//上位机进入运营锁车模式')
    communication_control_pub(container, mode='vehicle_mode', state='operation')

    # 上位机为运营锁车态
    if state_machine_state_echo(container) != 4:
        raise Exception('当前状态不为运营锁车')

    logging.info('2、下发解锁命令）'
                 '//状态机切换为运营就绪')
    communication_control_pub(container, mode='vehicle_state', state='unlock')

    # 查看状态机状态为运营就绪
    if state_machine_state_echo(container) != 5:
        raise Exception('当前状态不为运营就绪')

    logging.info('3、注入platform_datacollect_sensor_state故障,id65541'
                 '//上位机状态机切换为运营故障，下位机状态机切换为故障态')
    # 注入platform_datacollect_sensor_state故障,id65541
    fault_inject_pub(container,65541,1)

    # 上位机20s内进入运营故障
    for i in range(10):
        if state_machine_state_echo(container) != 8:
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
    if alarm_info['content'] != 'sensor_state collect failed' or alarm_info['type'] != '0':
        raise Exception('告警不正确')

    # 取消故障注入
    fault_inject_pub(container,65541,0)

    # 查看告警取消的信息
    alarm_info = communication_alarm_echo(container)
    if alarm_info['content'] != 'sensor_state collect failed' or alarm_info['type'] != '1':
        raise Exception('告警不正确')



























