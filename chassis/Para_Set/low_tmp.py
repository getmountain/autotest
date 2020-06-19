# coding:utf-8
import TX2
from Command.Container import Chassis
from Case_docker.lib.Chassis.fault_inject import chassis_alarm_echo,tp_main_set


ip = '0.0.0.0'
TX2 = TX2.TX2(ip)
containers = TX2.Containers()
container = TX2.Containers()['chassis_serial']
TX2.Images()
if len(containers) != 12:
    raise Exception('docker未全部启动')
if not Chassis.Exec(container).roscore_check():
    raise Exception('roscore未自动启动')

# data_value = "'set_env cpu_usage 25'"
# data = '"data: %s"' %data_value
# Chassis.Exec(container).rostopic_pub(topic='/chassis/cmd_req ',msg_type='std_msgs/String ',args=data)

tp_main_set(container,'5','1')
result = chassis_alarm_echo(container)
print(result)
# cpu_usage = re.search('cpu_usage:\s(\d+)',result).group(1)
tp_main_set(container,'5','0')
















