# coding: utf-8
import os
file = '/apollo/modules/planning/conf/planning_navi.conf'
old_str = '--navigation_mode_set_localization_timeout='
new_str = '--navigation_mode_set_localization_timeout=200000000\n'
with open(file, "r") as f1, open("%s.bak" % file, "w") as f2:
    for line in f1.readlines():
        if old_str in line:
            f2.write(new_str)
            continue
        f2.write(line)
os.remove(file)
os.rename("%s.bak" % file, file)

