import docker
import TX2

ip = '192.168.0.179'

def func(x):
    return x

def test_answer():
    #assert func(3) == 3
    # if func(3) != 3:
    #     raise Exception('ERROR')
    print 'start'
    a = TX2.TX2(ip)
    containers = a.Containers()
    assert len(containers) == 13
    print 'over'