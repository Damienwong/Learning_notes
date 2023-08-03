# -*- coding: utf-8 -*-
# @Time     : 2023/7/31 17:12
# @Author   : WHB
# @File     : png
# @Software : PyCharm

import pkgutil

data = pkgutil.get_data(__graphics.formats__, 'calibration.dat')
print(data)