# coding:utf-8
import TX2
import logging
from Command.Container import Chassis
import re
from Case_docker.lib.Chassis.Chassis_State import chassis_state_echo
'''
用例名称: 检查车架/chassis_state各项参数为默认值
前置步骤：所有docker均已启动。roscore已运行
测试步骤：1、查看当前状态/chassis_state
          //各项均为默认值（无故障切换状态）
作者:Li Siying
创建时间：2019-10-24
'''

# 测试数据
ip = '0.0.0.0'

# 测试步骤
def default_state():
    logging.info('前置步骤：所有docker均已启动。roscore已运行')
    tx2 = TX2.TX2(ip)
    containers = tx2.Containers()
    container = tx2.Containers()['chassis_serial']
    tx2.Images()
    if len(containers) != 11:
        raise Exception('docker未全部启动')
    if not Chassis.Exec(container).roscore_check():
        raise Exception('roscore未自动启动')

    logging.info('1、查看当前状态/chassis_state'
                 '//各项均为默认值（无故障切换状态）')
    result = chassis_state_echo(container=container)
    if int(result['cpu_usage']) >= 50:
        raise Exception('cpu占用超过80%')
    if result['wdg_state'] != '0':
        raise Exception('看门狗状态异常')
    if result['bms'] != '0':
        raise Exception('电源板异常')
    if result['motor'] != '0':
        raise Exception('电机异常')
    if result['motor_driver'] != '0':
        raise Exception('电驱异常')
    if result['joystick'] != '0':
        raise Exception('摇杆异常')
    if result['imu'] != '0':
        raise Exception('imu异常')
    if result['ultrasonic'] != '0':
        raise Exception('超声波异常')
    if result['ultrasonic'] != '0':
        raise Exception('超声波异常')
    if result['weighing'] != '0':
        raise Exception('重力系统异常')
    if result['flash'] != '0':
        raise Exception('flash异常')
    other_res = re.match('\[(\d+),\s(\d+),\s(\d+),\s(\d+),\s0',result['other_res']).groups()
    if other_res[0] != '0':
        raise Exception('网络通信异常')
    if other_res[1] != '0':
        raise Exception('led通信异常')
    if int(other_res[2]) >= 80:
        raise Exception('cpu温度过高')
    if int(other_res[3]) >= 80:
        raise Exception('imu温度过高')
    logging.info('检查完成，下位机各项指标均正常')

    print(result)
















