# coding:utf-8
import subprocess
from Command.Container import apollo_dev
from Case_docker.lib.Apollo import Rosbag_remap


def shell_exec(cmdline):
    '''
    执行shell命令并返回输出信息，
    shell返回值非0时会抛异常
    '''
    o = subprocess.check_output(cmdline, shell=True)
    return o


def clr_rosbag():
    '''
    清除apollo_dev中的rosbag包
    '''
    shell_exec('rm -rf /opt/autotest/bag/*')


def set_rosbag(resource):
    '''
    放置rosbag包到apollo_dev指定目录
    '''
    shell_exec('cp %s /opt/autotest/bag/ ' % resource)


def set_geofence(container, resource):
    '''
    配置自动驾驶参考线,重启fence模块
    '''
    shell_exec('cp %s /opt/autotest/routineCar/data/fence/geofence.json'%resource)
    restart_node_apollo(container, 'fence')


def set_refer_line(container, resource):
    '''
    配置自动驾驶参考线,重启relative_map模块
    '''
    shell_exec('cp %s /opt/autotest/reference_line/line.bag.txt.smoothed'%resource)
    restart_node_apollo(container, 'relative_map')


def set_localization(container):
    '''
    修改定位配置文件，忽略时间戳差异,重启定位模块
    '''
    apollo_dev.Exec(container).pycase(scpt='set_localization.py')
    restart_node_apollo(container, 'localization')


def set_planning(container):
    '''
    修改规划配置文件，忽略时间戳差异,重启规划模块
    '''
    apollo_dev.Exec(container).pycase(scpt='set_planning.py')
    restart_node_apollo(container, 'planning')


def restart_node_apollo(container,node):
    '''
    重启apollo模块，apollo容器里执行/apollo/scripts/下的脚本重启某个模块
    '''
    cmdline = "ps aux | grep %s | awk '{print $2}' |xargs  kill -9" % Rosbag_remap.node_script_apollo[node]
    apollo_dev.Exec(container).popen(Command=cmdline)



