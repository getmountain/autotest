# coding:utf-8
import TX2
from Command.Container import Chassis
import re

ip = '0.0.0.0'
TX2 = TX2.TX2(ip)
containers = TX2.Containers()
container = TX2.Containers()['chassis_serial']
TX2.Images()
if len(containers) != 12:
    raise Exception('docker未全部启动')
if not Chassis.Exec(container).roscore_check():
    raise Exception('roscore未自动启动')

data_value = "'set_env system_stack 20'"
data = '"data: %s"' %data_value
Chassis.Exec(container).rostopic_pub(topic='/chassis/cmd_req ',msg_type='std_msgs/String ',args=data)

result = Chassis.Exec(container).cmd_res_vf(isSET=True)
if result != '250':
    raise Exception('参数设置日志有误')

result = Chassis.Exec(container).rostopic_echo(topicName='/chassis_state')
stack_sensor = re.search('stack_sensor:\s(\d+)',result).group(1)
stack_comtrol = re.search('stack_sensor:\s(\d+)',result).group(1)
stack_cmm = re.search('stack_sensor:\s(\d+)',result).group(1)
if stack_sensor != '250' or stack_cmm != '250' or stack_comtrol != '250':
    raise Exception('预期值堆栈为250，实际值有误')

data_value = "'del_env system_stack'"
data = '"data: %s"' %data_value
Chassis.Exec(container).rostopic_pub(topic='/chassis/cmd_req ',msg_type='std_msgs/String ',args=data)

if not Chassis.Exec(container).cmd_res_vf(isSET=False):
    raise Exception('操作日志有误')

print('over')











