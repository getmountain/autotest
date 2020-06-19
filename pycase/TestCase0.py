#coding:utf-8
import unittest,sys
sys.path.append('/apollo/data/autotest/apotest')
from config.Case_Config import rosbag_play,listener,Config
from Command.apollo_dev import rosbag_info


config = Config('/apollo/data/autotest/apotest/guard/detect_guardian.config')
class Test(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass
    def test_cpu(self):
        assert 1 == 2 - 1
    def test_case(self):
        print(output.keys())
        # print('IMU LENTH IS : ', len(output['/imu']))
        # print('ODOM LENTH IS : ', len(output['/odom']))
        # print('UTL LENTH IS : ', len(output['/apollo/ultanalyse']))
        # print('GUAR LENTH IS : ', len(output['/apollo/guardian']))
        # assert len(output['/imu']) == int(rosbag_info(config.bagpath())['topics']['/imu'])
        # assert len(output['/odom']) == int(rosbag_info(config.bagpath())['topics']['/odom'])
        # assert len(output['/apollo/ultanalyse']) == int(rosbag_info(config.bagpath())['topics']['/apollo/ultanalyse'])
        # assert len(output['/apollo/guardian']) == int(rosbag_info(config.bagpath())['topics']['/apollo/guardian'])

if __name__ == '__main__':
    # 检测被测对象，停掉对应模块
    # if detect_Node.name == 'GUARDIAN':
    #     os.system('bash /apollo/scripts/ultanalyse.sh stop')
    #     os.system('bash /apollo/scripts/guardian.sh stop')
    rosbag_play(config.bagpath(),config.AllTopics())
    output = listener(config)
    suite = unittest.TestSuite()
    suite.addTest(Test('test_cpu'))
    suite.addTest(Test('test_case'))
    runner = unittest.TextTestRunner()
    runner.run(suite)
    # 测试完成后，重新启动所有模块
    # os.system('bash /apollo/start_apollo_sys.sh')




