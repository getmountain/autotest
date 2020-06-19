# coding:utf-8
import common.proto_utils as proto_utils
from gr_detect_module_config_pb2 import GRMDManagerConfig
import rospy
import time,os
from modules.guardian.proto.guardian_pb2 import GuardianCommand
import threading

# 读取配置文件，解析为proto格式
config_file = ''
# config_info = proto_utils.get_pb_from_text_file(config_file, GRMDManagerConfig())
# 配置回放的包
# bag = config_info.bagname
# 寻找包
# ModuleDataConfig.name = '/apollo/data/bag/' + bag_module + bag_id + '.bag'
# 监听话题
# ListenTopics = config_info.topics

# 回放包
def rosbag_play(module=None,bag_id=None):
    os.system('rosbag play ' + '/apollo/data/bag/2019-08-31-14-57-43_0.bag')
    # os.system('rosbag play %s' % bag)

i = 0
# 注册节点

infolist = []
def callback(a):
    global infolist
    rospy.loginfo(rospy.get_caller_id() + '我觉得 %s', a)#.header.sequence_num)
    TM = time.time
    infolist.append(a)

def listener():
    rospy.init_node('listener', anonymous=True)

    rospy.Subscriber('/apollo/guardian',data_class = 'pb_msgs/GuardianCommand', callback=callback)
    # rospy.Timer(rospy.Duration(1),callback)
    # rospy.spin()

    r = rospy.Rate(1)

    # while 1:
    #     num = len(infolist)
    #     r.sleep()
    #     if num == len(infolist) and num != 0:
    #         break

if __name__ == '__main__':
    # Thread1 = threading.Thread(target=listener)
    # Thread2 = threading.Thread(target=rosbag_play)
    # Thread1.start()
    # Thread2.start()
    # Thread1.setDaemon(True)
    # Thread2.setDaemon(True)
    # Thread1.join()
    # Thread2.join()
    listener()
    print('所有信息为: ')
    print(infolist)