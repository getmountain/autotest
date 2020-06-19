#coding:utf-8
import sys
sys.path.append('/apollo/data/autotest/apotest')
from config.Case_Config import rosbag_play,listener
from Command.tools.topic2dict import writetopic
import rospy,rosbag
from modules.ultanalyse.proto.ultanalyse_pb2 import ObstAnalyse,UltrasensorState
import time


if __name__ == '__main__':
    # out_file = {}
    bagpath = '/apollo/data/bag/2019-11-01-18-26-13_0.bag'
    bag = rosbag.Bag(bagpath)
    out_file = []
    for topic, msg_pb, t in bag.read_messages():
        if topic == '/apollo/ultanalyse':
            out_file.append(msg_pb)
    # 指定文件为执行py脚本传入的所有文件
    #navi_files = sys.argv[1:]
    # 注册一个节点，名字叫""，不自动生成名字（因为只有一个实例）
    rospy.init_node("lsy", anonymous=False)
    # 发布话题，名字叫""，数据类型为......,不同时发布
    ultanalyse_pub = rospy.Publisher(
        "/apollo/ultanalyse", ObstAnalyse, queue_size=1)

    insert_info = ObstAnalyse()
    header = insert_info.header
    header.timestamp_sec = 12345
    obs = insert_info.obstinfo.add()
    obs.location_x = 9999
    obs.location_y = 6666
    obs.detec_sonar = 11
    obs.obst_distance = 111.11

    out_file.append(insert_info)


    print('拢共有%d条信息'%len(out_file))
    r = rospy.Rate(20)
    for info in out_file:
        r.sleep()
        ultanalyse_pub.publish(info)


