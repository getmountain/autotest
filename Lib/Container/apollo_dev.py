# coding:utf-8
import re
from Command.Container import Exec_Run
import threading
import logging

attstr = '/bin/bash -c "source /home/tmp/ros/setup.bash \
                export PKG_CONFIG_PATH=/home/tmp/ros/lib/pkgconfig && \
                export PYTHONPATH=/usr/local/lib/python2.7/dist-packages:/apollo/py_proto:/usr/local/apollo/snowboy/Python:/apollo/modules/tools:/home/tmp/ros/lib/python2.7/dist-packages && \
                YOUR_CMD"'

class Exec(Exec_Run.Common):
    def __init__(self,dock):
        self.dock = dock

    def rosbag_info(self,bag):
        CmdBash = "'source /home/tmp/ros/setup.bash && rosbag info %s'" %bag
        # Cmd = "/bin/bash -c %s" %CmdBash
        Command = "/bin/bash -c %s" %CmdBash
        result = self.exec_common(Command).decode().split('\n')
        # result = self.dock.exec_run(Cmd,user='nvidia').output
        info = {}
        for line in result.split('\n')[0:8]:
            info[line.split(':')[0].strip()] = line.split(':')[1].strip()
        info['topics'] = {}
        Strtopics = result.split('topics:')[1]
        for topic in Strtopics.split('\n')[0:-1]:
            ParLine = re.search('(\S+)\s+(\d+)\smsgs', topic)
            info['topics'][ParLine.group(1)] = ParLine.group(2)
        return info

    def rostopic_list(self):
        Command = "/bin/bash -c 'source /home/tmp/ros/setup.bash && rostopic list'"
        result = self.exec_common(Command).decode().split('\n')
        # result = self.dock.exec_run(CmdBase,user='nvidia').output.decode().split('\n')
        return result


    def rostopic_echo(self, topicName, number):
        CmdBash = "'source /home/tmp/ros/setup.bash && rostopic echo -n %d %s'" % (number, topicName)
        # Cmd = "/bin/bash -c %s" % CmdBash
        Command = "/bin/bash -c %s" % CmdBash
        output = self.exec_common(Command)
        # output = self.dock.exec_run(Cmd, user='nvidia').output.decode()
        return output

    def rostopic_pub(self,topic,msg_type,args):
        Command = 'rostopic pub -1 %s %s %s' %(topic,msg_type,args)
        output = self.exec_common(Command)
        # output = self.dock.exec_run(attstr.replace('YOUR_CMD','rostopic pub -1 %s %s %s' %(topic,msg_type,args)), user='nvidia').output
        logging.info(str(output))
        if 'publishing and latching message for 3.0 seconds' not in str(output):
            raise Exception('发布失败')
        return str(output)

    def rosbag_play(self, bag):
        CmdBash = "'source /home/tmp/ros/setup.bash && rosbag play %s'" % bag
        # Cmd = "/bin/bash -c %s" % CmdBash
        Command = "/bin/bash -c %s" % CmdBash
        result = self.exec_common(Command)
        # result = self.dock.exec_run(Cmd, user='nvidia').output
        if 'Done.' not in result:
            raise Exception('error in playing bag')
        return result

    def rostopic_echo_bag(self,bag,topicName):
        Command = 'rostopic echo -b %s %s' %(bag,topicName)
        result = self.exec_common(Command)
        # result = self.dock.exec_run(attstr.replace('YOUR_CMD','rostopic echo -b %s %s' %(bag,topicName)), user='nvidia').output
        dataList = []
        for line in result.split('\n'):
            if 'data: ' in line:
                data = re.search('data: \[(.+)\]', line).group(1)
                dataList.append(data)
        return dataList
    '''
    def rostopic_echo_bag(self, bag, topicName):
        n = self.rosbag_info(bag=bag)['topics'][topicName]
        result = self.rostopic_echo(number=int(n), topicName=topicName)
        dataList = []
        for line in result.split('\n'):
            if 'data: ' in line:
                data = re.search('data: \[(.+)\]', line).group(1)
                dataList.append(data)
        return dataList

    def rosbag_topic(self,bag,topic):

        class MyThread(threading.Thread):
            def __init__(self, target=None, args=(), **kwargs):
                super(MyThread, self).__init__()
                self._target = target
                self._args = args
                self._kwargs = kwargs

            def run(self):
                if self._target == None:
                    return
                self.__result__ = self._target(*self._args, **self._kwargs)

            def get_result(self):
                self.join()  # 当需要取得结果值的时候阻塞等待子线程完成
                return self.__result__

        threads = []
        threads.append(MyThread(target=self.rosbag_play,args=([bag])))
        threads.append(MyThread(target=self.rostopic_echo_bag,args=(bag,topic)))
        threads[0].start()
        threads[1].start()
        threads[0].join()
        threads[1].join()
        return threads[1].get_result()
        '''
    def ultrasound_pub(self, datalist):
        if len(datalist) != 12:
            raise Exception('超声波数据格式错误')
        data = '"data: %s"' %datalist
        CmdBash = "'source /home/tmp/ros/setup.bash && rostopic pub -1 /ultrasound std_msgs/Int32MultiArray %s'" %data
        # Cmd = "/bin/bash -c %s" % CmdBash
        Command = "/bin/bash -c %s" % CmdBash
        output = self.exec_common(Command)
        # output = self.dock.exec_run(Cmd, user='nvidia').output
        if output != 'publishing and latching message for 3.0 seconds\n':
            raise Exception('pub fail')
        return output

    def ultanalyseInfo(self, number=1):
        Command = 'rostopic echo -n %d /apollo/ultanalyse' %number
        result = self.exec_common(Command)
        # result = self.dock.exec_run(attstr.replace('YOUR_CMD','rostopic echo -n %d /apollo/ultanalyse' %number), user='nvidia').output
        result = result.decode().replace('\n', ' ')
        Info = {}
        Info['header'] = {}
        headvaluestr = re.search('.+?{(.+?)}', result).group(1)
        groups = re.search('(\w+): (\S+)\s+(\w+): (\S+)\s+(\w+): (\d+)', headvaluestr)
        for i in range(1, 6, 2):
            Info['header'][groups.group(i)] = groups.group(i + 1)
        Info['obstinfos'] = re.findall('obstinfo { (.+?)}', result)
        if len(Info['obstinfos']) != 0:
            for i in range(len(Info['obstinfos'])):
                groups = re.search('(\w+): (\S+)\s+(\w+): (\S+)\s+(\w+): (\S+)\s+(\w+): (\S+)', Info['obstinfos'][i])
                Info['obstinfos'][i] = {}
                for j in range(1, 8, 2):
                    Info['obstinfos'][i][groups.group(j)] = groups.group(j + 1)
        return Info

    def pycase(self, scpt, path='/apollo/data/autotest/apotest/Command/tools/', para=''):
        Command = 'python ' + path + scpt + ' ' + para
        result = self.exec_common(Command)
        return result

    def popen(self,Command):
        result = self.exec_common(Command)
        return result

    def exec_common(self,CMD):
        logging.info(CMD)
        result = self.dock.exec_run(attstr.replace('YOUR_CMD',CMD), user='nvidia').output
        logging.info(result)
        return result