#coding:utf-8
import unittest,sys
sys.path.append('/apollo/data/autotest/apotest')
from config.Case_Config import rosbag_play,listener,Config
from Command.apollo_dev import rosbag_info


config = Config('/apollo/data/autotest/apotest/guard/detect_guardian.config')

rosbag_play(config.bagpath(),config.AllTopics())
output = listener(config)
print(output)