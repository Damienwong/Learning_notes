# -*- coding: utf-8 -*-
# @Time     : 2023/7/31 17:11
# @Author   : WHB
# @File     : fill
# @Software : PyCharm
import os
import sys

# sys.path.append('../formats')

current_dir = os.path.dirname(os.path.abspath(__file__))
print(current_dir)

abs_path = os.path.abspath(os.path.join(current_dir, '../formats'))

print(abs_path)

sys.path.append(abs_path)

import jpg