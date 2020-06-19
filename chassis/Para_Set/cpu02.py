# coding:utf-8
import TX2

ip = '192.168.0.179'
def data():
    global ip



def procedure():
    a = TX2.TX2(ip)
    containers = a.Containers()
    assert len(containers) == 13
    print 'over'











