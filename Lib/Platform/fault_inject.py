# coding:utf-8
import re
from Command.Container import Chassis
import time

def fault_inject_pub(container,tp_id,enable):
    '''
    下发故障注入命令，enable为1为注入，0为取消
    rostopic pub -1 /fault_inject std_msgs/Int32MultiArray -- """
    layout:
        dim: []
        data_offset: 0
    data: [65541, 0]
    """
    '''
    data = '"data: [%d, %d]"' %(tp_id,enable)
    Chassis.Exec(container).rostopic_pub(topic='/fault_inject',msg_type='std_msgs/Int32MultiArray ',args=data)


