# coding:utf-8
import common.proto_utils as proto_utils
import rospy, rosbag
import time, os, sys, re, unittest
from modules.guardian.proto.guardian_pb2 import GuardianCommand
from modules.ultanalyse.proto.ultanalyse_pb2 import ObstAnalyse
from nav_msgs.msg import Odometry
from sensor_msgs.msg import Imu
from std_msgs.msg import UInt8MultiArray

bagpath = '/apollo/data/bag/2019-07-18-17-20-48_0.bag'

bag = rosbag.Bag(bagpath)

ultrasoundInfo = []
for topic, message, t in bag.read_messages():
    if topic == '/ultrasound':
        ultrasoundInfo.append(message)

# UInt8MultiArray.
# print(dir(ultrasoundInfo[0]),ultrasoundInfo[0])
print(ultrasoundInfo[0])
DataList = []
for ultrasound in ultrasoundInfo:
    MSG = ''
    for i in ultrasound.data:
        MSG = MSG + str(ord(i)) + ','
    DataList.append(MSG)
print(len(DataList))
# print(len(UltanalyseInfo),UltanalyseInfo[0].header.timestamp_sec)
# rospy.init_node("lsy", anonymous=False)
# gps_pub = rospy.Publisher(
#     "/ultrasound", UInt8MultiArray, queue_size=1)
#
# r = rospy.Rate(1)
# for msg in ultrasoundInfo:
#     r.sleep()
#     gps_pub.publish(msg)print()