#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Author: haibo.wang
@Date: 2025/8/9
@Description: 
"""

import sys


def process_args():
    if len(sys.argv) < 4:
        print("用法: python script.py <名字> <年龄> <身高>")
        return

    name = sys.argv[1]

    try:
        age = int(sys.argv[2])
    except ValueError:
        print("错误: 年龄必须是整数")
        return

    try:
        height = float(sys.argv[3])
    except ValueError:
        print("错误: 身高必须是数字")
        return

    print(f"姓名: {name}")
    print(f"年龄: {age} 岁")
    print(f"身高: {height} 米")


if __name__ == "__main__":
    process_args()