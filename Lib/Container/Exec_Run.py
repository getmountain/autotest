# -*- coding:utf-8 -*-
import docker
import re
import logging

class Common(object):
    def __init__(self,dock):
        self.dock = dock

    def rostopic_list(self):
        '''
        显示rostopic list结果并返回
        '''
        CMD = 'rostopic list'
        output = self.exec_common(CMD).split('\n')
        # output = self.dock.exec_run('rostopic list').output.split('\n')
        return output

    def rostopic_echo(self,topicName):
        CMD = 'rostopic echo -n 1 ' + topicName
        output = self.exec_common(CMD)
        # output = self.dock.exec_run('rostopic echo -n 1 ' + topicName).output
        return output

    def roscore_check(self):
        CMD = 'roscore'
        output = self.exec_common(CMD)
        # output = self.dock.exec_run('roscore').output
        if 'roscore cannot run as another roscore/master is already running.' in str(output):
            return True
        return False

    def rostopic_pub(self,topic,msg_type,args):
        CMD = 'rostopic pub -1 ' + topic +' '+ msg_type +' '+ args
        output = self.exec_common(CMD)
        # output = self.dock.exec_run('rostopic pub -1 ' + topic +' '+ msg_type +' '+ args).output
        if 'publishing and latching message for 3.0 seconds' not in str(output):
            raise Exception('发布失败')
        return str(output)

    def rostopic_echo_bag(self,bag,topicName):
        CMD = 'rostopic echo -b ' + bag + ' ' +topicName
        result = self.exec_common(CMD)
        # result = self.dock.exec_run('rostopic echo -b ' + bag + ' ' +topicName).output
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
        CMD = 'rosservice call ' + service + ' ' +args
        result = self.exec_common(CMD)
        # result = self.dock.exec_run('rosservice call ' + service + ' ' +args).output
        return result

    def popen(self,CMD):
        result = self.exec_common(CMD)
        return result

    def exec_common(self,CMD):
        logging.info(CMD)
        result = self.dock.exec_run(CMD).output
        logging.info(str(result))
        return result

class Exec(Common):
    def __init__(self,dock):
        self.dock = dock

    def cmd_res_vf(self,isSET):
        output = self.dock.exec_run('rostopic echo -n 1 /chassis/cmd_res').output
        logging.info(output)
        if 'OK' not in output:
            raise Exception('命令下发失败')
        if isSET == True:
            return re.search('value\s=\s(\d+)',output).group(1)
        else:
            return True
