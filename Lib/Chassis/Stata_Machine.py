# coding:utf-8
import docker
import re
from Command.Container import Chassis

def chassis_control_state_pub(container,operation):
    '''
    操作operation对应的命令
    0 上锁..............................................lock
    1 解锁..............................................unlock
    2 停车..............................................stop
    3 手动驾驶..........................................manual
    4 自动驾驶..........................................auto
    5 故障..............................................fault
    6 故障恢复（故障->锁车）............................fault_rec
    '''
    OperationList = ['lock','unlock','stop','manual','auto','fault','fault_rec']
    data = OperationList.index(operation)
    msg = '"data: %s"' % str(data)
    Chassis.Exec(container).rostopic_pub(topic='/chassis/control_state ', msg_type='std_msgs/UInt8 ', args=msg)

def chassis_state_change_echo(container):
    result = Chassis.Exec(container).rostopic_echo(topicName='/chassis/state_change')
    state = re.search('.+(\d+)', str(result)).group(1)
    #state_str=re.search('data:.+(\d+)', str(result)).group()#add_by_xxq
    #state = re.search('.+(\d+)', str(state_str)).group(1)#add_by_xxq
    return int(state)
