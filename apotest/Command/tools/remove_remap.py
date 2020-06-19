# coding: utf-8
import sys
# 将文件读进列表(反复追加)中：
lines = []
with open(sys.argv[1], "r") as y:
    for line in y.readlines():
        if ':=' in line:
            continue
        lines.append(line)
    y.close()

# 写到文件中去：
with open(sys.argv[1], "w") as z:
    for line in lines:
        z.writelines(line)

