from config import gr_detect_module_config_pb2 as gb
# 写
nodeL = gb.NodeData()
nodeL.name = 'LSY'
nodeL.type = 1
nodeL.detect_type = 2
nodeL.delay_tolerance = 3

INFO = nodeL.SerializeToString()
print(INFO)
# 读
RD = gb.NodeData()
RD.ParseFromString(INFO)
print(RD.name)
print(RD.type)
print(RD.detect_type)
print(RD.delay_tolerance)

