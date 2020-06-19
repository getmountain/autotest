#!/usr/bin/env python
# coding:utf-8

import rospy
import common.proto_utils as proto_utils
from modules.localization.proto.localization_pb2 import LocalizationEstimate


file = '/apollo/data/autotest/pycase/1_localization.pb.txt'


if __name__ == '__main__':
    # 指定文件为执行py脚本传入的所有文件
    #navi_files = sys.argv[1:]
    # 注册一个节点，名字叫""，不自动生成名字（因为只有一个实例）
    rospy.init_node("lsy", anonymous=False)
    # 发布话题，名字叫""，数据类型为......,不同时发布
    gps_pub = rospy.Publisher(
        "/apollo/localization/pose", LocalizationEstimate, queue_size=1)

    # 传入的第二个参数文件localization_pb_file
    localization_pb_file = file
    # 阿波罗自带解析，将指定文件转换为需要的proto格式
    localization_pb = proto_utils.get_pb_from_text_file(
        localization_pb_file, LocalizationEstimate())

    gps_info = LocalizationEstimate()
    gps_info.pose.position.x = localization_pb.pose.position.x

while True:
    r = rospy.Rate(1)  # 0.5hz
    r.sleep()
    gps_pub.publish(gps_info)
    r.sleep()

