#coding:utf-8
import sys
sys.path.append('/apollo/data/autotest/apotest')
from config.Case_Config import rosbag_play,listener
from Command.tools.topic2dict import writetopic

path_prefix = sys.argv[1]
bagpath = sys.argv[2]
output_topic = sys.argv[3]

rosbag_play(bagpath,sys.argv[4:])
output = listener(bagpath,sys.argv[3:])
# 指定观察的话题
output_topic_info = output[output_topic]
# 指定生成话题信息的文件
with open(path_prefix + 'real.txt', "w") as f:
    f.write(str(output_topic_info))
    f.close()
with open(path_prefix + 'output.txt', "w") as f:
    f.write(str(output))
    f.close()
# 指定读取bag包中的话题
writetopic(bag=bagpath,topic=output_topic,path=path_prefix)





