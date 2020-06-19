# coding:utf-8
from Command.Container import Exec_Run
import re
import logging

class Exec(Exec_Run.Common):
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