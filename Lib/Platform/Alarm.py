# coding:utf-8
import docker
import re
from Command.Container import Chassis

def self_check_service(container):
    '''
    rosservice rosservice call /self_check "req: '{\"check_mode\"}'"
    对影响状态机的自检结果解析,返回告警列表
    '''
    service = '/self_check'
    args = r'''"req: '{\"check_mode\":1}'"'''
    result = Chassis.Exec(container).rosservice_call(service,args).decode()
    idList = re.findall('\d{7,}',result)
    return idList

def alarm_mask(container,id=0):
    '''
    rostopic pub -1 /alarm_mask std_msgs/UInt32 "data: 0"
    按ID屏蔽告警，默认0屏蔽所有告警
    '''
    Chassis.Exec(container).rostopic_pub(topic='alarm_mask',msg_type='std_msgs/UInt32',
                                         args='"data: %d"' %id)

def alarm_command(container, id=0,mask_state='true',check_mask='true'):
    '''
    rosservice call /alarm_command "req: '{\"alarm_command\":{\"id\":33649089,\"mask_state\":true,\"check_mask\":true}}'"
    check_mask:为True时查询已屏蔽的告警列表。为False时才识别告警ID和屏蔽恢复动作
    id:告警ID
    mask_state：为'true'时屏蔽，'false'为恢复
    '''
    service = '/alarm_command'
    args = r'''"req: '{\"alarm_command\":{\"id\":%d,\"mask_state\":%s,\"check_mask\":%s}}'"'''%(id,mask_state,check_mask)
    result = Chassis.Exec(container).rosservice_call(service,args).decode()
    if check_mask == True:
        idList = re.findall('\d{7,}',result)
        return idList

def communication_alarm_echo(container):
    '''
    查看上报给pad的最新一次告警.返回字典，包含模块，告警id，type和告警内容信息
    type为0表示注入，1表示恢复
    '''
    result = Chassis.Exec(container).rostopic_echo(topicName='/communication/alarm').decode().replace('\\','')
    info = {}
    info['id'] = re.search('id\":(\d+)',result).group(1)
    info['type'] = re.search('type\":(\d+)',result).group(1)
    info['content'] = re.search('content\":\"(.+?)\"',result).group(1)
    info['module'] = re.search('module\":\"(\w+)',result).group(1)
    return info