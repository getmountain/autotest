import os
os.chdir('/home/nvidia/work/data/autotest/Case_docker/Chassis/Chassis_State/')
os.system('python3 test_Chassis_State.py')
os.chdir('/home/nvidia/work/data/autotest/Case_docker/Chassis/fault_inject/')
os.system('python3 test_Fault_CI.py')