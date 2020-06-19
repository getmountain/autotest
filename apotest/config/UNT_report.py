# coding:utf-8
import unittest

class Test(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass
    def test_cpu(self):
        assert 1 == 2-1
    def test_cpu1(self):
        assert 1 == 2-0

if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(Test('test_cpu'))
    suite.addTest(Test('test_cpu1'))
    runner = unittest.TextTestRunner()
    runner.run(suite)
    # filepath = 'result.html'
    # fp = open(filepath,'wb')
    # runner = HTMLTestRunner.HTMLTestRunner(stream=fp,title='title',description='test')
    # runner.run(suite)
    # fp.close()