#!/usr/bin/env python
# coding:utf-8

import sys
import rospy
#import common.proto_utils as proto_utils
from modules.localization.proto.localization_pb2 import LocalizationEstimate
import json
import time

# if len(sys.argv) != 2:
#     print "no file specified"
#     sys.exit()
#
# localization_pb_file = sys.argv[1]
# localization_pb = proto_utils.get_pb_from_text_file(
#     localization_pb_file, Gps())
# current_t = localization_pb.header.timestamp_sec
#
# 发布话题，名字叫""，数据类型为......,不同时发布
# destination_pub = rospy.Publisher(
#     "/apollo/vechile_destination", Gps, queue_size=1)
# # 生成目的地信息
# destination_info = Gps()

if __name__ == '__main__':
    # 指定文件为执行py脚本传入的所有文件
    #navi_files = sys.argv[1:]
    # 注册一个节点，名字叫""，不自动生成名字（因为只有一个实例）
    rospy.init_node("lsy", anonymous=False)
    # 发布话题，名字叫""，数据类型为......,不同时发布
    gps_pub = rospy.Publisher(
        "/apollo/localization/pose", LocalizationEstimate, queue_size=1)

    gps_info = LocalizationEstimate()
    header = gps_info.header
    header.timestamp_sec = time.time()
    header.module_name = 'localization'
    header.sequence_num = 1

    pose = gps_info.pose
    position = pose.position
    position.x = 10
    position.y = 11
    position.z = 12

    gps_info2 = LocalizationEstimate()
    header = gps_info2.header
    header.timestamp_sec = time.time()
    header.module_name = 'localization'
    header.sequence_num = 2

    pose = gps_info2.pose
    position = pose.position
    position.x = 20
    position.y = 21
    position.z = 22

    r = rospy.Rate(1)  # 0.5hz
    for info in [gps_info,gps_info2]:
        r.sleep()
        gps_pub.publish(info)


