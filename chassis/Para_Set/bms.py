# coding:utf-8
import TX2
from Command.Container import Exec_Run
import re

bms_val = ''
ip = '192.168.0.179'
TX2 = TX2.TX2(ip)
containers = TX2.Containers()
container = TX2.Containers()['chassis_serial']
TX2.Images()
if len(containers) != 13:
    raise Exception('docker未全部启动')
if not Exec_Run.Common(container).roscore_check():
    raise Exception('roscore未自动启动')

data_value = "'set_env bms 0'"
data = '"data: %s"' %data_value
Exec_Run.Common(container).rostopic_pub(topic='/cmd_req ',msg_type='std_msgs/String ',args=data)

result = Exec_Run.Common(container).rostopic_echo(topicName='/chassis_state')
bms = re.search('bms:\s(\d+)',result).group(1)
if bms != '0':
    raise Exception('预期值为0，实际值为'+bms)











