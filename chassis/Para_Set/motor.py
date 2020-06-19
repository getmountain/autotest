# coding:utf-8
import TX2
from Command.Container import Chassis
import re

ip = '192.168.0.179'
TX2 = TX2.TX2(ip)
containers = TX2.Containers()
container = TX2.Containers()['chassis_serial']
TX2.Images()
if len(containers) != 13:
    raise Exception('docker未全部启动')
if not Chassis.Exec(container).roscore_check():
    raise Exception('roscore未自动启动')

data_value = "'set_env motor_state 1'"
data = '"data: %s"' %data_value
Chassis.Exec(container).rostopic_pub(topic='/chassis/cmd_req ',msg_type='std_msgs/String ',args=data)

result = Chassis.Exec(container).cmd_res_vf(isSET=True)
if result != '1':
    raise Exception('参数设置日志有误')

result = Chassis.Exec(container).rostopic_echo(topicName='/chassis_state')
motor = re.search('motor:\s(\d+)',result).group(1)
if motor != '1':
    raise Exception('预期值为1，实际值为'+motor)

data_value = "'del_env motor_state'"
data = '"data: %s"' %data_value
Chassis.Exec(container).rostopic_pub(topic='/chassis/cmd_req ',msg_type='std_msgs/String ',args=data)

if not Chassis.Exec(container).cmd_res_vf(isSET=False):
    raise Exception('操作日志有误')

print 'over'











