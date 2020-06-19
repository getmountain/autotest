#coding:utf-8
import unittest,sys
sys.path.append('/apollo/data/autotest/apotest')
from config.Case_Config import rosbag_play,listener,Config,Bag_Read_message
from Command.apollo_dev import rosbag_info

config = Config('/apollo/data/autotest/apotest/Planning/detect_planning.config')

class Test(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass
    def test_cpu(self):
        assert 1 == 2 - 1
    def test_case(self):
        Planning_info = reaily.TopicInfo(config.AllTopics())['/apollo/planning']
        Exp_Planning_info = output['/apollo/planning']
        assert Planning_info == Exp_Planning_info
if __name__ == '__main__':
    # 检测被测对象，停掉对应模块
    # if detect_Node.name == 'GUARDIAN':
    #     os.system('bash /apollo/scripts/ultanalyse.sh stop')
    #     os.system('bash /apollo/scripts/guardian.sh stop')
    reaily = Bag_Read_message(config.bagpath())
    print(reaily)
    rosbag_play(config.bagpath(),config.AllTopics()[1:])
    output = listener(config)
    suite = unittest.TestSuite()
    suite.addTest(Test('test_cpu'))
    suite.addTest(Test('test_case'))
    runner = unittest.TextTestRunner()
    runner.run(suite)
    # 测试完成后，重新启动所有模块
    # os.system('bash /apollo/start_apollo_sys.sh')


