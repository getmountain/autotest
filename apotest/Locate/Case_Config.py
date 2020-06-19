from config.gr_detect_module_config_pb2 import ModuleDataConfig
import rospy
import time,os

# 配置回放的包
bag_module = 'control_planning'
bag_id = '1'
# 寻找包
ModuleDataConfig.name = '/apollo/data/bag/' + bag_module + bag_id + '.bag'
# 监听话题
ListenTopics = [1,2]
# 回放包
os.system('')

i = 0
# 注册节点
def callback(topic):
    global TM
    rospy.loginfo(rospy.get_caller_id() + '我觉得 %s', topic.header.sequence_num)
    TM = time.time

def listener():
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber('/apollo/localization/pose', ModuleDataConfig, callback)
    rospy.spin()

if __name__ == '__main__':
    listener()