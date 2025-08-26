#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Author: haibo.wang
@Date: 2025/8/22
@Description: 
"""


import argparse


# 创建ArgumentParse对象
parser = argparse.ArgumentParser(description='This is an example.')

# 添加参数
parser.add_argument('--input', '-i', type=str, required=True, help='输入文件路径')
parser.add_argument('--output', '-o', type=str, default='output.txt', help='输出文件路径')
parser.add_argument('--verbose', '-v', action='store_true', help='详细模式')
parser.add_argument('--count', '-c', type=int, default=1, help='重复次数')
parser.add_argument('name', type=str, help='name')

# 解析参数
args = parser.parse_args()

# 使用参数
print(f'输入文件：{args.input}')
print(f'输出文件：{args.output}')
print(f'详细模式：{args.verbose}')
print(f'重复次数：{args.count}')
print(f'名字：{args.name}')
