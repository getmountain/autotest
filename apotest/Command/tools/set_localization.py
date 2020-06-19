# coding: utf-8
import os
file = '/apollo/modules/localization/conf/localization.conf'
tar = '--pf_gps_time_sync=true'
with open(file, "a+") as f:
    num = f.read().count(tar)
    if num == 1:
        f.write(tar)


