# coding:utf-8
import unittest
import cpu_usage_class
from cpu01 import cpu_01
from cpu02 import procedure
import pytest

class Test(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass
    def test_cpu01(self):
        cpu_01
    def test_cpu02(self):
        procedure()
if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTests((Test('test_cpu01'),Test('test_cpu02')))

    runner = unittest.TextTestRunner()
    runner.run(suite)
    # filepath = 'result.html'
    # fp = open(filepath,'wb')
    # runner = HTMLTestRunner.HTMLTestRunner(stream=fp,title='title',description='test')
    # runner.run(suite)