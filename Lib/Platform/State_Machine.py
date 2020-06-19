import docker
import re,logging
from Command.Container import Chassis
from Case_docker.lib.Platform.Alarm import alarm_command,alarm_mask,self_check_service

def communication_control_pub(container,mode,state):
    '''
    rostopic pub -1 /communication/control std_msgs/String
    "data: '{\"message_id\":1,\"from\":\"pad\",\"to\":\"control\",
    \"state_change\":{\"vehicle_state\":\"lock\"}}'"
    使用从pad发出的通信层命令切换状态机状态
    mode : vehicle_mode/vehicle_state
    state: operation/maintenance/lock/unlock/ready/auto
    '''

    # CMD = r'''rostopic pub -1 /communication/control std_msgs/String
    # "data: '{\"message_id\":1,\"from\":\"pad\",\"to\":\"control\",
    # \"state_change\":{\"%s\":\"%s\"}}'"''' %(mode,state)
    # # container.exec_run(CMD)
    data = r'''"data: '{\"message_id\":1,\"from\":\"pad\",\"to\":\"control\",\"state_change\":{\"%s\":\"%s\"}}'"''' %(mode,state)
    Chassis.Exec(container).rostopic_pub(topic='/communication/control',msg_type='std_msgs/String ',args=data)
    #logging.info("当前状态为:"+str(state_machine_state_echo(container)))

def state_machine_state_echo(container):
    '''
    查看上位机状态机的状态
    '''
    result = Chassis.Exec(container).rostopic_echo(topicName='/state_machine/state')
    state = re.search('.+(\d+)', str(result)).group(1)
    return int(state)

def change_vehicle_state(container,state,times=2):
    '''
    检查上位机从任意状态切换为目标态，指定次数内成功返回True,否则返回Flase
    '''
    if state == state_machine_state_echo(container):
        logging.info("state ready")
        return
    # 首先初始化为维护锁车态。任意状态下，屏蔽告警->停车->锁车->切维护模式可达到维护锁车态
    logging.info("clear alarm list")
    cur_state = state_machine_state_echo(container)
    logging.info("当前状态为:"+str(cur_state)+"，目标状态为:"+str(state))
    i = 0
    while i < times:
        id_list = self_check_service(container)
        if id_list:
            for alarm_id in id_list:
                alarm_mask(container, int(alarm_id))
            for alarm_id in id_list:
                alarm_command(container,id=int(alarm_id),mask_state='false',check_mask='false')
        logging.info("clear all alarm ok")
        communication_control_pub(container, mode='vehicle_state', state='ready')
        communication_control_pub(container, mode='vehicle_state', state='lock')
        communication_control_pub(container, mode='vehicle_mode', state='maintenance')
        if state_machine_state_echo(container) != 0:
            i = i+1
            if i == times:
                raise Exception('初始化状态机为维护锁车态失败')
            logging.warning('第%d次初始化状态机为维护锁车态失败'%i)
            continue
        if state == 1:
            communication_control_pub(container, mode='vehicle_state', state='unlock')
        elif state == 4:
            communication_control_pub(container, mode='vehicle_mode', state='operation')
        elif state == 5:
            communication_control_pub(container, mode='vehicle_mode', state='operation')
            communication_control_pub(container, mode='vehicle_state', state='unlock')
        elif state == 7:
            communication_control_pub(container, mode='vehicle_mode', state='operation')
            communication_control_pub(container, mode='vehicle_state', state='unlock')
            communication_control_pub(container, mode='vehicle_state', state='auto')
        i = i+1
        if i == times:
            if state != state_machine_state_echo(container):
                raise Exception('切换目标状态失败')
        else:
            if state != state_machine_state_echo(container):
                logging.warning('第%d次切换状态机失败'%i)
                continue
        break
