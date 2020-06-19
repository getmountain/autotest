# coding:utf-8
import TX2

class cpu_01():
    def data(self):
        self.ip = '192.168.0.179'

    def procedure(self):
        a = TX2.TX2(self.ip)
        containers = a.Containers()
        assert len(containers) != 13
        print 'over'











