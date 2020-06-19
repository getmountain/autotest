# coding:utf-8
import TX2
from Command.Container import Chassis
import re

ip = '192.168.0.179'

class TestClass:
    def func(x):
        return x

    def test_answer(self):
        tx2 = TX2.TX2(ip)
        container = tx2.Containers()['chassis_serial']
        if not Chassis.Exec(container).roscore_check():
            raise Exception('roscore未自动启动')