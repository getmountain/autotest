# !/usr/bin/env python
# coding=utf-8

import time
import rospy
from modules.localization.proto.localization_pb2 import LocalizationEstimate

infolist = []
def callback(LocalizationEstimate):
    global infolist
    rospy.loginfo(rospy.get_caller_id() + '我觉得 %s', LocalizationEstimate)#.header.sequence_num)
    TM = time.time
    infolist.append(LocalizationEstimate)

def listener():
    rospy.init_node('listener', anonymous=True)

    rospy.Subscriber('/apollo/localization/pose', LocalizationEstimate, callback)
    # rospy.Timer(rospy.Duration(1),callback)
    # rospy.spin()

    r = rospy.Rate(1)

    while 1:
        num = len(infolist)
        r.sleep()
        if num == len(infolist) and num != 0:
            break

if __name__ == '__main__':
    listener()
    print('所有信息为: ')
    print(infolist)