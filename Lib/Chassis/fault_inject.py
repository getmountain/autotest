# coding:utf-8
import re
from Command.Container import Chassis
import time

def chassis_alarm_echo(container):
    '''
    返回chassis_alarm的一次结果,类型为字典
    header:
    seq: 23703
    stamp:
    secs: 2066
    nsecs: 514321000
    frame_id: ''
    system_alarm: 32768
    motor_alarm: 0
    motor_driver_alarm: 0
    external_sensor_alarm: 0
    internal_sensor_alarm: 0
    power_alarm: 0
    '''
    time.sleep(2)
    result = str(Chassis.Exec(container).rostopic_echo(topicName='/chassis_alarm'))
    output = {}
    List = result.split("\\n")
    for Line in List:
        line = Line.strip()
        if ": " in line:
            output[line.split(': ')[0]] = line.split(': ')[1]
    return output

def tp_main_set(container,eTP_num,switch):
    '''
    通过/chassis/cmd_req设置TP点,例如：
    rostopic pub -1 /chassis/cmd_req std_msgs/String "data: 'tp_main set_tp 5 1'"
    '''
    data_value = "tp_main set_tp %s %s" %(eTP_num,switch)
    data = '"data: %s"' % data_value
    Chassis.Exec(container).rostopic_pub(topic='/chassis/cmd_req',msg_type='std_msgs/String ',args=data)

def tp_main_get(container,eTP_num):
    '''
    通过/chassis/cmd_req查询TP点状态,例如：
    rostopic pub -1 /chassis/cmd_req std_msgs/String "data: 'tp_main get_tp 5'"
    '''
    data_value = "tp_main get_tp %s" %eTP_num
    data = '"data: %s"' % data_value
    Chassis.Exec(container).rostopic_pub(topic='/chassis/cmd_req',msg_type='std_msgs/String ',args=data)

def chassis_alarm_check(container):
    '''
    检查chassis_alarm的一次结果,为默认值返回True，否则返回False
    system_alarm: 0
    motor_alarm: 0
    motor_driver_alarm: 0
    external_sensor_alarm: 0
    internal_sensor_alarm: 0
    power_alarm: 0
    '''
    result = chassis_alarm_echo(container)
    for value in result.values():
        if value != '0':
            raise Exception("当前存在异常告警")
    return True
