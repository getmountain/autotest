#coding:utf-8
import unittest,sys
sys.path.append('/apollo/data/autotest/apotest')
from config.Case_Config import rosbag_play,listener,Config,Bag_Read_message
from Command.apollo_dev import rosbag_info

config = Config('/apollo/data/autotest/apotest/Guardian/detect_guardian.config')
class Test(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass
    def test_cpu(self):
        assert 1 == 2 - 1
    def test_case(self):
        for key in reaily:
            print(key,len(reaily[key]))
        # for key in output.keys():
        #     if output.get(key):
        #         print(key)
        # Guardian_info = reaily.TopicInfo(config.AllTopics())['/apollo/guardian']
        # Exp_Guardian_info = output['/apollo/guardian']
        # assert Guardian_info == Exp_Guardian_info

        # Guardian_info = reaily.TopicInfo(config.AllTopics())['/platform/platform_guardian']
        # Exp_Guardian_info = output['/platform/platform_guardian']
        # assert Guardian_info == Exp_Guardian_info
if __name__ == '__main__':
    # 检测被测对象，停掉对应模块
    # if detect_Node.name == 'GUARDIAN':
    #     os.system('bash /apollo/scripts/ultanalyse.sh stop')
    #     os.system('bash /apollo/scripts/guardian.sh stop')
    reaily = Bag_Read_message(config.bagpath()).TopicInfo(config.AllTopics())
    # rosbag_play(config.bagpath(),config.AllTopics()[2:])
    # output = listener(config)
    suite = unittest.TestSuite()
    suite.addTest(Test('test_cpu'))
    suite.addTest(Test('test_case'))
    runner = unittest.TextTestRunner()
    runner.run(suite)
    # 测试完成后，重新启动所有模块
    # os.system('bash /apollo/start_apollo_sys.sh')


