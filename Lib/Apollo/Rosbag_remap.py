# coding:utf-8
import docker
import re
from Command.Container import apollo_dev
from Command.Container import Chassis

node_script_apollo = {
        'gnss': 'gps_proc.sh',
        'msg_transformer': 'msg_transformer_proc.sh',
        'planning': 'navigation_planning_proc.sh',
        'speedlimit': 'speedlimit_proc.sh',
        'guardian': 'guardian_proc.sh',
        'fence': 'fence_proc.sh',
        'control': 'navigation_control_proc.sh',
        'localization': 'navigation_localization_proc.sh',
        'perception': 'navigation_perception_proc.sh',
        'ultanalyse': 'ultanalyse_proc.sh',
        'command_handler': 'command_handler_proc.sh',
        'prediction': 'navigation_prediction_proc.sh',
        'relative_map': 'relative_map_tx2_proc.sh',
        'monitor': 'monitor_proc.sh',
        'navigator': 'reference_line_proc.sh',
        }

def topic_mask(container,node,topic,Newtopic=None):
    '''
    修改/apollo/scripts/下的_proc文件，remap原有输入话题
    '''
    proc =  node_script_apollo[node]
    if not Newtopic:
        apollo_dev.Exec(container).pycase(scpt='file_insert.py',para='/apollo/scripts/%s %s:=/New%s' %(proc,topic,topic))
    else:
        apollo_dev.Exec(container).pycase(scpt='file_insert.py',para='/apollo/scripts/%s %s:=%s' %(proc,topic,Newtopic))

def recover_topic_mask(container,node):
    '''
    恢复修改/apollo/scripts/下的_proc文件，取消remap原有输入话题
    '''
    if node == 'gnss':
        proc = 'gps_proc.sh'
    if node == 'msg_transformer':
        proc = 'msg_transformer_proc.sh'
    if node == 'planning':
        proc = 'navigation_planning_proc.sh'
    if node == 'speedlimit':
        proc = 'speedlimit_proc.sh'
    if node == 'guardian':
        proc = 'guardian_proc.sh'
    if node == 'fence':
        proc = 'fence_proc.sh'
    if node == 'control':
        proc = 'navigation_control_proc.sh'
    if node == 'localization':
        proc = 'navigation_localization_proc.sh'
    if node == 'perception':
        proc = 'navigation_perception_proc.sh'
    if node == 'ultanalyse':
        proc = 'ultanalyse_proc.sh'
    if node == 'command_handler':
        proc = 'command_handler_proc.sh'
    if node == 'prediction':
        proc = 'navigation_prediction_proc.sh'
    if node == 'relative_map':
        proc = 'relative_map_tx2_proc.sh'
    if node == 'monitor':
        proc = 'monitor_proc.sh'
    if node == 'navigator':
        proc = 'reference_line_proc.sh'
    apollo_dev.Exec(container).pycase(scpt='remove_remap.py',para='/apollo/scripts/%s' %proc)

def set_chassis_serial(container):
    '''
    remap下位机传感器的/imu,/odom,/ultrasound,/chassis/control_info话题
    '''
    file = '/opt/routineCar/src/platform_vehicle/models/chassis_serial/launch/node.launch'
    content = '"<launch> \
    <node pkg=\\"chassis_serial\\" type=\\"chassis_serial_node\\" name=\\"chassis_serial_node\\" respawn =\\"true\\"> \
        <param name=\\"port\\" value=\\"/dev/tty_chassis\\"/> \
		 <remap from=\\"/imu\\" to=\\"/imu_\\"/> <remap from=\\"/odom\\" to=\\"/odom_\\"/> <remap from=\\"/chassis/control_info\\" to=\\"/chassis/control_info__\\"/><remap from=\\"/ultrasound\\" to=\\"/ultrasound_\\"/> \
    </node> \
    </launch>"'
    Chassis.Exec(container).popen("bash -c 'echo %s > %s'"%(content,file))

def recover_chassis_remap(container):
    '''
    恢复remap下位机传感器的/imu,/odom,/ultrasound,/chassis/control_info话题
    '''
    file = '/opt/routineCar/src/platform_vehicle/models/chassis_serial/launch/node.launch'
    content = '"<launch> \
    <node pkg=\\"chassis_serial\\" type=\\"chassis_serial_node\\" name=\\"chassis_serial_node\\" respawn =\\"true\\"> \
        <param name=\\"port\\" value=\\"/dev/tty_chassis\\"/> \
    </node> \
    </launch>"'
    Chassis.Exec(container).popen("bash -c 'echo %s > %s'"%(content,file))



