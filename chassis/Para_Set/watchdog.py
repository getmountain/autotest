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

data_value = "'set_env watchdog_cfg 1'"
data = '"data: %s"' %data_value
Chassis.Exec(container).rostopic_pub(topic='/chassis/cmd_req ',msg_type='std_msgs/String ',args=data)

result = Chassis.Exec(container).cmd_res_vf(isSET=True)
if result != '1':
    raise Exception('参数设置日志有误')

result = Chassis.Exec(container).rostopic_echo(topicName='/chassis_state')
watchdog = re.search('wdg_state:\s(\d+)',result).group(1)
if watchdog != '0':
    raise Exception('看门狗状态未复位')

print 'over'











