# coding:utf-8
import docker
import re,os
from Command.Container import apollo_dev
from Command.Container import Chassis

def geofence_switch(container,switch):
    '''
    设置地理围栏开关，0为关闭，1为打开
    rostopic pub /apollo/switch_req std_msgs/String "data: '{\"geofence_switch\":0}'"
    '''
    if switch == 0:
        data = r'''\"data: '{\\\"geofence_switch\\\":0}'\"'''
    elif switch == 1:
        data = r'''\"data: '{\\\"geofence_switch\\\":1}'\"'''
    else:
        raise Exception('请输入开关值0或1')
    apollo_dev.Exec(container).rostopic_pub(topic='/apollo/switch_req',msg_type='std_msgs/String',args=data)



