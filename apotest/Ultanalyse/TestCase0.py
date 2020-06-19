#coding:utf-8
import unittest,sys
sys.path.append('/apollo/data/autotest/apotest')
from config.Case_Config import rosbag_play,listener,Config,Bag_Read_message
from Command.apollo_dev import rosbag_info

config = Config('/apollo/data/autotest/apotest/Ultanalyse/detect_ultanalyse.config')

class Test(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass
    def test_cpu(self):
        assert 1 == 2 - 1
    def test_case(self):
        Ultanalyse_info = reaily.TopicInfo(config.AllTopics())['/apollo/ultanalyse']
        Exp_Ultanalyse_info = output['/apollo/ultanalyse']
        assert Ultanalyse_info == Exp_Ultanalyse_info

        Ultrasound_down_info = reaily.TopicInfo(config.AllTopics())['/apollo/ultrasound_down']
        Exp_Ultrasound_down_info = output['/apollo/ultrasound_down']
        assert Ultrasound_down_info == Exp_Ultrasound_down_info

if __name__ == '__main__':
    # 检测被测对象，停掉对应模块
    # if detect_Node.name == 'GUARDIAN':
    #     os.system('bash /apollo/scripts/ultanalyse.sh stop')
    #     os.system('bash /apollo/scripts/guardian.sh stop')
    reaily = Bag_Read_message(config.bagpath())
    rosbag_play(config.bagpath(),config.AllTopics()[2:])
    output = listener(config)
    suite = unittest.TestSuite()
    suite.addTest(Test('test_cpu'))
    suite.addTest(Test('test_case'))
    runner = unittest.TextTestRunner()
    runner.run(suite)
    # 测试完成后，重新启动所有模块
    # os.system('bash /apollo/start_apollo_sys.sh')


