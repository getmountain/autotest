# !/usr/bin/env python
# coding=utf-8

import time
import rospy
from modules.localization.proto.localization_pb2 import LocalizationEstimate


def callback(LocalizationEstimate):
    global TM
    rospy.loginfo(rospy.get_caller_id() + '我觉得 %s', LocalizationEstimate.header.sequence_num)
    TM = time.time

def listener():
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber('/apollo/localization/pose', LocalizationEstimate, callback)
    rospy.spin()

if __name__ == '__main__':
    listener()
