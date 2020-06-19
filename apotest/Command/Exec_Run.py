# -*- coding:utf-8 -*-
import docker
import re
import logging


def rostopic_list(self):
    '''
    显示rostopic list结果并返回
    '''
    output = self.dock.exec_run('rostopic list').output.split('\n')
    return output

def rostopic_echo(self,topicName):
    output = self.dock.exec_run('rostopic echo -n 1 ' + topicName).output
    logging.info(str(output))
    return output

def roscore_check(self):
    output = self.dock.exec_run('roscore').output
    logging.info(str(output))
    if 'roscore cannot run as another roscore/master is already running.' in str(output):
        return True
    return False

def rostopic_pub(self,topic,msg_type,args):
    output = self.dock.exec_run('rostopic pub -1 ' + topic +' '+ msg_type +' '+ args).output
    logging.info(str(output))
    if 'publishing and latching message for 3.0 seconds' not in str(output):
        raise Exception('发布失败')
    return str(output)

def rostopic_echo_bag(self,bag,topicName):
    result = self.dock.exec_run('rostopic echo -b ' + bag + ' ' +topicName).output
    dataList = []
    for line in result.split('\n'):
        if 'data: ' in line:
            data = re.search('data: \[(.+)\]', line).group(1)
            dataList.append(data)
    return dataList

def rosservice_call(self,service,args):
    '''
    Usage: rosservice call /service [args...]
    '''
    result = self.dock.exec_run('rosservice call ' + service + ' ' +args).output
    logging.info(str(result))
    return result

