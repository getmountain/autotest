# coding:utf-8
import TX2
from Command.Container import Exec_Run
import re

ip = '192.168.0.179'
TX2 = TX2.TX2(ip)
containers = TX2.Containers()
container = TX2.Containers()['chassis_serial']
TX2.Images()
if len(containers) != 13:
    raise Exception('docker未全部启动')
if not Exec_Run.Common.roscore_check():
    raise Exception('roscore未自动启动')

result = Exec_Run.Common(container).rostopic_echo(topicName='/chassis_state')
bms = re.search('bms:\s(\d+)',result).group(1)
print bms










