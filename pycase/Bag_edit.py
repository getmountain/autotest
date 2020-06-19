# coding:utf-8
import common.proto_utils as proto_utils
import rospy, rosbag
import time, os, sys, re, unittest
from modules.guardian.proto.guardian_pb2 import GuardianCommand
from modules.ultanalyse.proto.ultanalyse_pb2 import ObstAnalyse
from nav_msgs.msg import Odometry
from sensor_msgs.msg import Imu

bagpath = '/apollo/data/bag/2019-07-18-17-20-48_0.bag'

bag = rosbag.Bag(bagpath)

UltanalyseInfo = []
for topic, message, t in bag.read_messages():
    if topic == '/apollo/ultanalyse':
        UltanalyseInfo.append(message)

# UltanalyseInfo[0].header.timestamp_sec = 9527
# print(len(UltanalyseInfo),UltanalyseInfo[0])

# print(len(UltanalyseInfo),UltanalyseInfo[0].header.timestamp_sec)
rospy.init_node("lsy", anonymous=False)
# 发布话题，名字叫""，数据类型为......,不同时发布
gps_pub = rospy.Publisher(
    "/apollo/ultanalyse", ObstAnalyse, queue_size=1)

gps_info = UltanalyseInfo[-1]
gps_info.header.timestamp_sec = 9527

r = rospy.Rate(1)
for  msg in UltanalyseInfo:
    r.sleep()
    gps_pub.publish(msg)
