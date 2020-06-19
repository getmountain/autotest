# coding:utf-8
import common.proto_utils as proto_utils
import gr_detect_module_config_pb2 as gr_pb
import rospy,rosbag
import time,os,sys
from modules.guardian.proto.guardian_pb2 import GuardianCommand
import threading
from MessageType import MessageType
#
# print("aaa")
# # 读取配置文件，解析为proto格式
# config_file = sys.argv[1]
# geshi = gr_pb.GRMDManagerConfig()
# # config_info = proto_utils.get_pb_from_text_file(config_file, geshi)
# proto_utils.get_pb_from_file(config_file, geshi)
# ListenTopic = geshi.config[0].node[0].type
# # print(geshi.config[0].node[0].type)
# print(MessageType[ListenTopic])

# 解析rosbag包
bagpath = '/apollo/data/bag/2019-08-31-14-57-43_0.bag'
bag = rosbag.Bag(bagpath)
# print(bag.read_messages())
for a,b,c in bag.read_messages():
    print(type(b))
# for i in bag.get_type_and_topic_info().topics:
#     print(bag.get_type_and_topic_info().topics[i])