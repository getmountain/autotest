# coding:utf-8
import time,os,sys,re,unittest
import logging
import common.proto_utils as proto_utils
from gr_detect_module_config_pb2 import GRMDManagerConfig
import rospy,rosbag
from modules.localization.proto.localization_pb2 import LocalizationEstimate
sys.path.append('/apollo/data/autotest/apotest')
sys.path.append('/apollo/data/autotest')

# 获取包的时间
def bag_play_duration(bag):
    bg = rosbag.Bag(bag)
    duration = bg.get_end_time() - bg.get_start_time()
    play_duration = duration + 5
    return play_duration

def rosbag_play(bag,topics,uSEC=30,delay=5):
    argvtopic = ''
    for topic in topics:
        argvtopic = argvtopic + topic + ' '
    CMD = 'rosbag play -u %d -d %d %s --topics %s  &' %(uSEC,delay,bag,argvtopic)
    print(CMD)
    os.popen(CMD)
    print('start play bag')

localization_info = []

def callback(message):
    global infolist
    rospy.loginfo(rospy.get_caller_id() + '我觉得 %s', message)
    infolist.append(message)

def localization_callback(msg):
    global localization_info
    localization_info.append(msg)

def ros_timer_events(msg):
    data = '"data: [17235969, 0]"'
    CMD = 'rostopic pub -1 ' + '/fault_inject' + ' ' + 'std_msgs/Int32MultiArray' + ' ' + data
    os.popen(CMD)
    print('FAULT INJECT:',CMD)
    rospy.signal_shutdown('Time out')

def fault_inject(msg):
    data = '"data: [17235969, 1]"'
    CMD = 'rostopic pub -1 ' + '/fault_inject' + ' ' + 'std_msgs/Int32MultiArray' + ' ' + data
    os.popen(CMD)
    print('FAULT INJECT:',CMD)

def listener(bagpath,duration=100):
    rospy.init_node('NODE', anonymous=True)
    rospy.Subscriber('/apollo/localization/pose', LocalizationEstimate, localization_callback)
    if not duration:
        duration = bag_play_duration(bagpath)
    rospy.Timer(rospy.Duration(duration), ros_timer_events)
    rospy.Timer(rospy.Duration(20), fault_inject)
    rospy.spin()
    return localization_info

bagpath = sys.argv[1]
output_topic = '/apollo/localization/pose'

rosbag_play(bagpath,topics=['/imu','/odom','/apollo/sensor/gnss/odometry'],uSEC=60)
output = listener(bagpath,duration=60)

# 指定生成话题信息的文件
with open('localization_pose.txt', "w") as f:
    f.write(str(output))
    f.close()