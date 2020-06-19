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

result = Exec_Run.Common(container).rostopic_echo(topicName='/fault_detect/event')
result = result.replace('\\','').replace('\n','')
result = re.search('data: (.+)---',result).group(1)
if result == '0':
    print '当前驾驶模式为can not move'
elif result == '1':
    print '当前驾驶模式为only manual'
elif result == '2':
    print '当前驾驶模式为can auto'
elif result == '3':
    print '当前驾驶模式为chassis interrupt'
else:
    raise Exception('echo结果有误')


