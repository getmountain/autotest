# coding:utf-8
import TX2
import time,os
import logging
from Lib.Container import Exec_Run
import re
from Lib.Chassis.fault_inject import tp_main_set,tp_main_get
'''
用例名称: 注入下位机复位TP点，下位机复位
前置步骤：所有docker均已启动。roscore已运行
测试步骤：1、注入下位机复位TP点
          //查看cmd_res返回set_tp OK id: 0,enable: 1
          2、5秒钟后，查询TP点状态
          //恢复为enable: 0   
作者:Li Siying
创建时间：2019-06-26
'''

class Test_eTP_000():
    def setup_method(self):
        logging.info('---------before----------')
        self.ip = '0.0.0.0'
        tx2 = TX2.TX2(self.ip)
        self.containers = tx2.Containers()
        self.container = tx2.Containers()['chassis_serial']
    def teardown_method(self):
        logging.info('---------after-----------')
        tp_main_set(self.container, '0', '0')
    # 测试步骤
    def test_eTP_000(self):
        logging.info('1、注入下位机复位TP点'
                     '//查看cmd_res返回set_tp OK id: 0,enable: 1')
        tp_main_set(self.container,'0','1')
        result = Exec_Run.Common(self.container).rostopic_echo(topicName='/chassis/cmd_res')
        if 'OK id: 0,enable: 1' not in str(result):
            raise Exception('tp点注入失败')

        logging.info('2、15秒钟后，查询TP点状态'
                     '//恢复为enable: 0')
        time.sleep(15)
        tp_main_get(self.container,'0')
        result = Exec_Run.Common(self.container).rostopic_echo(topicName='/chassis/cmd_res')
        if 'main_board get_tp OK id: 0,enable: 0' not in str(result):
            raise Exception('下位机重启后未恢复')














