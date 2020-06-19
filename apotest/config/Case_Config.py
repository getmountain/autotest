# coding:utf-8
import common.proto_utils as proto_utils
from gr_detect_module_config_pb2 import GRMDManagerConfig
import rospy,rosbag
import time,os,sys,re,unittest
from nav_msgs.msg import Odometry
from sensor_msgs.msg import Imu,Image
from std_msgs.msg import UInt8MultiArray,Float64MultiArray,Float32MultiArray,String
from geometry_msgs.msg import Twist
from MessageType import MessageType
from Command.apollo_dev import rosbag_info
from modules.guardian.proto.guardian_pb2 import GuardianCommand,UltrasensorConfig
from modules.ultanalyse.proto.ultanalyse_pb2 import ObstAnalyse,UltrasensorState
from modules.localization.proto.localization_pb2 import LocalizationEstimate
from modules.planning.proto.planning_pb2 import ADCTrajectory
from modules.map.relative_map.proto.navigation_pb2 import MapMsg
from modules.canbus.proto.chassis_pb2 import Chassis
from modules.prediction.proto.prediction_obstacle_pb2 import PredictionObstacles
from modules.control.proto.control_cmd_pb2 import ControlCommand
from modules.perception.proto.perception_obstacle_pb2 import PerceptionObstacles
from modules.localization.proto.gps_pb2 import Gps
from modules.fence.proto.fence_pb2 import FenceCmd
from modules.control.proto.control_cmd_pb2 import ControlCommand


class Config():
    def __init__(self,config):
        self.config_info = proto_utils.get_pb_from_text_file(config, GRMDManagerConfig())
    def bagpath(self):
        bagpath = '/apollo/data/bag/' + self.config_info.config[0].name
        return bagpath
    def Nodes(self):
        # 注册监听节点
        Nodes = self.config_info.config[0].node
        return Nodes
    def detect_Node(self):
        detect_Node = self.Nodes()[0]
        return detect_Node
    def AllTopics(self):
        # 配置文件的所有话题
        AllTopics = []
        for Node in self.Nodes():
            AllTopics.append(MessageType[Node.type])
        return AllTopics
    def InputTopics(self):
        # 输入话题
        InputTopics = self.AllTopics[self.config_info.config[0].InputNum:]
        return InputTopics
    def OutputTopics(self):
        # 输出话题
        OutputTopics = self.AllTopics[0:self.config_info.config[0].InputNum]
        return OutputTopics

class Bag_Read_message():
    def __init__(self,bagpath):
        self.bag_info = rosbag.Bag(bagpath)
    def TopicInfo(self,topics):
        TopicInfo = {}
        for ReplayTopic in topics:
            TopicInfo[ReplayTopic] = []
        for topic,message,t in self.bag_info.read_messages():
            for ReplayTopic in topics:
                if topic == ReplayTopic:
                    TopicInfo[ReplayTopic].append(message)
        return TopicInfo

# 获取包的时间
def bag_play_duration(bag):
    bg = rosbag.Bag(bag)
    duration = bg.get_end_time() - bg.get_start_time()
    play_duration = duration + 5
    return play_duration

def rosbag_play(bag,topics,startSEC=0):
    argvtopic = ''
    for topic in topics:
        argvtopic = argvtopic + topic + ' '
    os.popen('rosbag play -s %d %s --topics %s  &' %(startSEC,bag,argvtopic))

odom_info = []
imu_info = []
ultanalyse_info = []
guardian_info = []
localization_info = []
planning_info = []
relative_map_info = []
canbus_info = []
prediction_info = []
control_info = []
perception_info = []
zed_info = []
ultrasound_info = []
ultrasound_down_info = []
ultrasensor_config_info = []
ultrasensor_state_info = []
platform_guardian_info = []
gnss_odometry_info = []
fence_info = []
control_info_info = []
cmd_vel_info = []
chassis_speed_limit_info = []
switch_req_info = []
switch_res_info = []

def callback(message):
    global infolist
    rospy.loginfo(rospy.get_caller_id() + '我觉得 %s', message)
    infolist.append(message)

def guardian_callback(msg):
    global guardian_info
    guardian_info.append(msg)

def imu_callback(msg):
    global imu_info
    imu_info.append(msg)

def odom_callback(msg):
    global odom_info
    odom_info.append(msg)

def ultanalyse_callback(msg):
    global ultanalyse_info
    ultanalyse_info.append(msg)

def planning_callback(msg):
    global planning_info
    planning_info.append(msg)

def localization_callback(msg):
    global ultanalyse_info
    ultanalyse_info.append(msg)

def relative_map_callback(msg):
    global relative_map_info
    #relative_map_info.append(msg)

def prediction_callback(msg):
    global prediction_info
    prediction_info.append(msg)

def control_callback(msg):
    global control_info
    control_info.append(msg)

def perception_callback(msg):
    global perception_info
    perception_info.append(msg)

def zed_callback(msg):
    global zed_info
    zed_info.append(msg)

def ultrasound_callback(msg):
    global ultrasound_info
    ultrasound_info.append(msg)

def ultrasound_down_callback(msg):
    global ultrasound_down_info
    ultrasound_down_info.append(msg)

def ultrasensor_config_callback(msg):
    global ultrasensor_config_info
    ultrasensor_config_info.append(msg)

def ultrasensor_state_callback(msg):
    global ultrasensor_state_info
    ultrasensor_state_info.append(msg)

def platform_guardian_callback(msg):
    global platform_guardian_info
    platform_guardian_info.append(msg)
    platform_guardian_info.append(time.time())

def gnss_odometry_callback(msg):
    global gnss_odometry_info
    gnss_odometry_info.append(msg)

def canbus_callback(msg):
    global canbus_info
    canbus_info.append(msg)

def fence_vel_callback(msg):
    global fence_info
    fence_info.append(msg)

def control_info_callback(msg):
    global control_info_info
    control_info_info.append(msg)

def cmd_vel_callback(msg):
    global cmd_vel_info
    cmd_vel_info.append(msg)
    cmd_vel_info.append(time.time())

def chassis_speed_limit_callback(msg):
    global chassis_speed_limit_info
    chassis_speed_limit_info.append(msg)
    chassis_speed_limit_info.append(time.time())

def switch_req_callback(msg):
    global switch_req_info
    switch_req_info.append(msg)

def switch_res_callback(msg):
    global switch_res_info
    switch_res_info.append(msg)

def ros_timer_events(msg):
    rospy.signal_shutdown('Time out')

def listener(bagpath,topics,duration=None):
    # bag_read = Bag_Read_message(config.bagpath())
    rospy.init_node('NODE', anonymous=True)

    for topic in topics:
        if topic == '/apollo/guardian':
            # print('topic is :'+ topic +'  type is  : ',type(bag_read.TopicInfo(config.AllTopics())[topic]))
            rospy.Subscriber(name = topic, data_class=GuardianCommand, callback=guardian_callback)
        if topic == '/imu':
            rospy.Subscriber(topic, Imu, imu_callback)
        if topic == '/odom':
            rospy.Subscriber(topic,Odometry, odom_callback)
        if topic == '/apollo/ultanalyse':
            rospy.Subscriber(topic, ObstAnalyse, ultanalyse_callback)
        if topic == '/apollo/localization/pose':
            rospy.Subscriber(topic, LocalizationEstimate, localization_callback)
        if topic == '/apollo/planning':
            rospy.Subscriber(topic, ADCTrajectory, planning_callback)
        if topic == '/apollo/relative_map':
            rospy.Subscriber(topic, MapMsg, relative_map_callback)
        if topic == '/apollo/canbus/chassis':
            rospy.Subscriber(topic, Chassis, canbus_callback)
        if topic == '/apollo/prediction':
            rospy.Subscriber(topic, PredictionObstacles, prediction_callback)
        if topic == '/apollo/control':
            rospy.Subscriber(topic,ControlCommand , control_callback)
        if topic == '/apollo/perception/obstacles':
            rospy.Subscriber(topic, PerceptionObstacles, perception_callback)
        if topic == '/apollo/sensor/camera/obstacle/front_6mm':
            rospy.Subscriber(topic, Image, zed_callback)
        if topic == '/ultrasound':
            rospy.Subscriber(topic, UInt8MultiArray, ultrasound_callback)
        if topic == '/ultrasound_down':
            rospy.Subscriber(topic, UInt8MultiArray, ultrasound_down_callback)
        if topic == '/apollo/ultrasensor_config':
            rospy.Subscriber(topic, UltrasensorConfig, ultrasensor_config_callback)
        if topic == '/apollo/ultrasensor_state':
            rospy.Subscriber(topic, UltrasensorState, ultrasensor_state_callback)
        if topic == '/platform/platform_guardian':
            rospy.Subscriber(topic, UInt8MultiArray, platform_guardian_callback)
        if topic == '/apollo/sensor/gnss/odometry':
            rospy.Subscriber(topic, Gps, gnss_odometry_callback)
        if topic == '/fence_vel':
            rospy.Subscriber(topic, FenceCmd, fence_vel_callback)
        if topic == '/chassis/control_info':
            rospy.Subscriber(topic, Float64MultiArray, control_info_callback)
        if topic == '/cmd_vel':
            rospy.Subscriber(topic, Twist, cmd_vel_callback)
        if topic == '/chassis/speed_limit':
            rospy.Subscriber(topic, Float32MultiArray, chassis_speed_limit_callback)
        if topic == '/apollo/switch_req':
            rospy.Subscriber(topic, String, switch_req_callback)
        if topic == '/apollo/switch_res':
            rospy.Subscriber(topic, String, switch_res_callback)
 
    if not duration:
        duration = bag_play_duration(bagpath)
    rospy.Timer(rospy.Duration(duration), ros_timer_events)
    rospy.spin()

    OutPut = {'/imu':imu_info,'/odom':odom_info,'/apollo/guardian':guardian_info,'/apollo/ultanalyse':ultanalyse_info,
              '/apollo/localization/pose':localization_info,'/apollo/planning':planning_info,'/apollo/relative_map':relative_map_info,
              '/apollo/canbus/chassis':canbus_info,'/apollo/prediction':prediction_info,'/apollo/control':control_info,
              '/apollo/perception/obstacles':perception_info,'/apollo/sensor/camera/obstacle/front_6mm':zed_info,
              '/ultrasound':ultrasound_info,'/ultrasound_down':ultrasound_down_info,'/apollo/ultrasensor_config':ultrasensor_config_info,'/apollo/ultrasensor_state':ultrasensor_state_info,
              '/platform/platform_guardian':platform_guardian_info,'/apollo/sensor/gnss/odometry':gnss_odometry_info,
              '/fence_vel':fence_info,'/chassis/control_info':control_info_info,'/cmd_vel':cmd_vel_info,'/chassis/speed_limit':chassis_speed_limit_info,
              '/apollo/switch_req':switch_req_info,'/apollo/switch_res':switch_res_info}

    return OutPut