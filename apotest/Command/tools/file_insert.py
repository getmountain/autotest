# coding: utf-8
import sys
# 将文件读进列表(反复追加)中：
lines = []
with open(sys.argv[1], "r") as y:
    for line in y.readlines():
        if ':=' not in line:
            lines.append(line)
    y.close()

# 在列表中插入文本数据：
lines.insert(-1, sys.argv[2]+' \\ \n')
s = ''.join(lines)

# 写到文件中去：
with open(sys.argv[1], "w") as z:
    z.write(s)
    z.close()

