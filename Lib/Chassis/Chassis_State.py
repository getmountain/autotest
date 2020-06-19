# coding:utf-8
import docker
import re
from Command.Container import Chassis

def chassis_state_echo(container):
    '''
    返回chassis_state的一次结果,类型为字典
    seq: 1251
    secs: 10290
    nsecs: 199577000
    frame_id: ''
    stack_sensor: 137
    stack_control: 137
    stack_comm: 345
    stack_rec: [165, 697, 0, 0, 0]
    cpu_usage: 25
    wdg_state: 0
    bms: 0
    motor: 0
    motor_driver: 0
    joystick: 0
    imu: 0
    ultrasonic: 8152
    weighing: 0
    flash: 0
    other_res: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    '''
    result = str(Chassis.Exec(container).rostopic_echo(topicName='/chassis_state'))
    output = {}
    List = result.split("\\n")
    for Line in List:
        line = Line.strip()
        if ": " in line:
            output[line.split(': ')[0]] = line.split(': ')[1]
    return output


