# -*- coding: utf-8 -*-

# a = 2.3
# r1 = isinstance(a, int)
# r2 = isinstance(a, float)
# r3 = isinstance(a, (str, float, list))
# print(r1, r2, r3)

import struct
# bits = b'\x4f\xfc\x0a'
# RX_temp = struct.unpack('<h',bits[0:2])
# RX_temp = RX_temp[0]/100
# print(RX_temp)


# string3 = str(bits)
# print(type(string3), string3)
# struct.unpack('6B', string3)

# raw_cmd_code = 256
# cmd_code1 = struct.pack('>H', raw_cmd_code)
# cmd_code2 = struct.pack('<H', raw_cmd_code)
# print(type(cmd_code1), cmd_code1)
# print(type(cmd_code2), cmd_code2)
# a = hex(255)
# b = hex(256)
# print(type(a), a)
# print(type(b), b)

# b = 256
# str1 = '0x{:04x}'.format(b)
# print(type(str1), str1)
# bits = bytes.fromhex(str1[2:])
# print(type(bits), bits)

# a = int.from_bytes(bytes=b'\x01\x02', 'big')
# b = int.from_bytes(bytes=b'\x01\x02', '')
# print(a)

# import struct
# bits = b'\x0212'
# a = struct.unpack('<h', bits)
# b = struct.unpack('>h', bits)
# print(type(a), a[0])  # unpack函数返回tuple
# print(type(b), b[0])
# print(type(a[0]))

# a = '0xff'
# b = '1ff'
# print(int(a, base=16))
# print(int(b, base=16))

# import struct
#
# raw_cmd_code = 256
# cmd_code1 = struct.pack('>H', raw_cmd_code)
# cmd_code2 = struct.pack('<H', raw_cmd_code)
# print(type(cmd_code1), cmd_code1)
# print(type(cmd_code2), cmd_code2)
#
# print(struct.pack('<2H', 1, 255))
# print(struct.pack('>LL', 1, 255))

# import struct
# bits = b'\x01\02'
# a = struct.unpack('<h', bits)
# b = struct.unpack('>h', bits)
# c = struct.unpack('<2B', bits)
# d = struct.unpack('>BB', bits)
# print(type(a), a[0])  # unpack函数返回tuple
# print(type(b), b[0])
# # print(type(c), c)
# print(type(d), d)

# string1 = 'aabbcc0102ff'
# bits = bytes().fromhex(string1)  # 字符串转化为字节流
# print(type(bits), bits)
#
# string2 = bits.hex()  # 字节流转化为字符串
# print(type(string2), string2)

# bits = b'\x01\x02'
# a = int.from_bytes(bits, byteorder='big')
# b = int.from_bytes(bits, 'little')
# print(type(a), a)
# print(type(b), b)

# print(hex(255))
# print(b'\xff'.hex())

# a = 60  # a = 0011 1100
# b = 13  # b = 0000 1101
#
# print('与运算结果：', a & b)
# print('或运算结果：', a | b)
# print('取反运算结果：', ~a)  # 对数据的每个二进制位取反，得到一个有符号二进制数的补码形式。 最终结果类似-a-1
# print('异或运算结果：', a ^ b)  # 当两对应的二进制位相异时，结果为1. 0011 0001 =  49
# print('左移位运算结果：', a << 2)  # 各二进制位全部左移若干位，高位丢弃，低位补0. 1111 0000
# print('右移位运算结果：', b >> 2)  # 各二进制位全部右移若干位  0000 0011
#
# print(a and b)  # 如果 x 为 False，x and y 返回 False，否则它返回 y 的计算值。
# print(a or b)  # 如果 x 是非 0，它返回 x 的计算值，否则它返回 y 的计算值。
# print(not a)  # 如果 x 为 True，返回 False 。如果 x 为 False，它返回 True。
#
# print('取余结果：', a % b)
# print('整除取整：', a // b)

# import struct
#
# input_file = r"D:\WORK\0_QT128相关\QT128_四色板.pcap"
# file_handle = open(input_file, 'rb')
# datas=''
# for j in range(16):
#     for i in range(8):
#         data = file_handle.read(1)
#         data_hex = str(hex(struct.unpack('<B', data)[0]))[2:]
#         if len(data_hex) == 1:
#             data_hex = '0'+data_hex
#         datas += data_hex
#     datas +='\n'
#
# print(datas)

# import hashlib
#
# m = hashlib.sha256()
# m.update(b"this is a test")
# # m.update(b" the spammish repetition")
# print(m.digest())
# print(m.digest().hex())
# print(len(m.digest().hex()))
#
#
# print(m)

# d = {} # 一个普通的字典
# d.setdefault('a', []).append(1)
# d.setdefault('a', []).append(2)
# d.setdefault('b', []).append(4)
# print(d)


# for i in "python":
#     if i == "t":
#         continue
#     print(i, end="")

# for i in "python":
#     if i == "t":
#         break
#     print(i, end="")

#
# for i in "python":
#     if i == "t":
#         break
#     print(i, end="")
# else:
#     print("程序正常退出")

# s1 = '{:#08x}'.format(15)
# s2 = '{:#8x}'.format(15)
#
# s3 = '0x{:08x}'.format(15)
# s4 = '0x{:8x}'.format(15)
#
# print(' s1: {}\n'.format(s1),
#       's2: {}\n'.format(s2),
#       's3: {}\n'.format(s3),
#       's4: {}\n'.format(s4))

# from collections import deque
# q = deque([0, 1, 2, 3, 4])
# print(5 in q)
# print(4 in q)
#
# # 顺时针
# q = deque([0, 1, 2, 3, 4])
# q.rotate(2)
# print('顺时针: ', q)
#
# # 逆时针
# q = deque([0, 1, 2, 3, 4])
# q.rotate(-2)
# print('逆时针: ', q)
#
# # extend
# q = deque([0, 1, 2, 3, 4])
# q.extend([5, 6, 7])
# print('extend: ', q)
#
# # extendleft
# q = deque([0, 1, 2, 3, 4])
# q.extendleft([0, -1, -2])
# print('extend: ', q)
# print(q.index(-2, 0, 2))  # 指定查找区间


# q = deque(maxlen=3)
# q.append([1, 2, 3])
# q.append('s')
# q.append(15)
# print(q)
#
# q.append(b'\x01')
# print(q)
#
# q.appendleft(0)
# print(q)
# # 增加
# q.append(5)
# print(q)
#
# # 从左侧增加
# q.appendleft(0)
# print(q)
#
# # 删除
# q.pop()
# print(q)
#
# # 删除左侧
# q.popleft()
# print(q).

# for i in range(127, -1, -1):
#     print(i)

# from collections import defaultdict
# s = defaultdict(dict)
# for i in range(1, 129):
#     s[i] = defaultdict(list)
# s[3]['B'].append(3)
# s[3]['B'].append(4)
# print(s)
# a = {'A': [3]}
# b = {'A': [4]}
#
# print(a + b)
# import csv
#
# # def write_csv_header(header, savefile):
# #     with open(savefile, 'w', encoding='utf8', newline='') as csvfile:
# #         myWrite = csv.writer(csvfile)
# #         myWrite.writerow(header)
#
# def write_n_row_to_csv(csv_rows, savefile):
#     with open(savefile, 'a+', encoding='utf8', newline='') as csvfile:
#         myWriter = csv.writer(csvfile)
#         for csv_row in csv_rows:
#             myWriter.writerow(csv_row)
#
# # write_csv_header(['A', 'B', 'C'], r'D:\WORK\00_QT64相关\Parse_check\123.csv')
# write_n_row_to_csv([[1, 2, 3]], r'D:\WORK\00_QT64相关\Parse_check\123.csv')
#
# # write_csv_header(['A', 'B', 'C'], r'D:\WORK\00_QT64相关\Parse_check\123.csv')
# write_n_row_to_csv([[4, 5, 6]], r'D:\WORK\00_QT64相关\Parse_check\123.csv')

# AT128_UDP_Struct = np.dtype([
#         ('pre-header', [
#             ('start_str', 'S2'),
#             ('major_version', 'u1'),
#             ('minor_version', 'u1'),
#             ('header_reserved', 'u2')]
#          ),
#
#         ('header', [
#             ('laser_num', 'u1'),
#             ('block_num', 'u1'),
#             ('first_block_return', 'u1'),
#             ('distance_unit', 'u1'),
#             ('return_number', 'u1'),
#             ('flags', 'u1')]
#          ),
#
#         ('body', [
#             ('block', [
#                 ('azimuth', 'u2'),
#                 ('fine_azimuth', 'u1'),
#                 ('dis_ref', [
#                     ('distance', 'u2'),
#                     ('reflectivity', 'u1'),
#                     ('confidence', 'u1')],
#                  128)],
#              2),
#             ('CRC1', 'u4')]
#          ),
#
#         ('tail', [
#             ('reserved1', '<u2'),
#             ('reserved1_id', 'u1'),
#             ('reserved2', '<u2'),
#             ('reserved2_id', 'u1'),
#             ('high_t_shutdown', 'u1'),
#             ('reserved3-1', 'u1'),
#             ('reserved3-2', 'u1'),
#             ('reserved3-3', 'u1'),
#             ('reserved4', 'u1'),
#             ('reserved5', 'u1'),
#             ('reserved6', 'u1'),
#             ('reserved7', 'u1'),
#             ('reserved8', 'u1'),
#             ('reserved9', 'u1'),
#             ('reserved10', 'u1'),
#             ('reserved11', 'u1'),
#             ('motor_speed', '<i2'),
#             ('timestamp', 'u4'),
#             ('return_mode', 'u1'),
#             ('factory_info', 'u1'),
#             ('utc_year', 'u1'),
#             ('utc_month', 'u1'),
#             ('utc_day', 'u1'),
#             ('utc_hour', 'u1'),
#             ('utc_min', 'u1'),
#             ('utc_sec', 'u1'),
#             ('udp_sequence', 'u4'),
#             ('crc', 'u4'),
#             ('signature', 'S32')]
#          )
#     ])

import heapq
# nums = [21, 34, 0.2, -4, -5, 3, 1, 100, 100]
# print(heapq.nlargest(3, nums))
# print(heapq.nsmallest(4, nums))
import heapq
# portfolio = [
#     {'name': 'IBM', 'shares': 100, 'price': 91.1},
#     {'name': 'AAPL', 'shares': 50, 'price': 543.22},
#     {'name': 'FB', 'shares': 200, 'price': 21.09},
#     {'name': 'HPQ', 'shares': 35, 'price': 31.75},
#     {'name': 'YHOO', 'shares': 45, 'price': 16.35},
#     {'name': 'ACME', 'shares': 75, 'price': 115.65}
# ]
# cheap = heapq.nsmallest(3, portfolio, key=lambda s: s['price'])
# expensive = heapq.nlargest(3, portfolio, key=lambda s: s['price'])
# print(cheap)
# print(expensive)

# nums = [1, 8, 2, 23, 7, -4, 18, 23, 42, 37, 2]
# import heapq
# heapq.heapify(nums)
# print(nums)

# nums = [1, 8, 2, 23, 7, -4, 18, 23, 42, 37, 2]
# import heapq
# heapq.heapify(nums)
# print(nums)
# # 查找最小的3个函数
# print(heapq.heappop(nums))
# print(heapq.heappop(nums))
# print(heapq.heappop(nums))

# a = '    spacious     '
# print(type(a))
# print(a.strip())
#
# s = 'www.example.com'
# print(s.strip('w.moc'))

# prices = {
#     'ACME': 45.23,
#     'AAPL': 612.78,
#     'IBM': 205.55,
#     'HPQ': 37.20,
#     'FB': 10.75
# }
#
# prices_and_names = zip(prices.values(), prices.keys())
# print(min(prices_and_names))
#
# print(sorted(prices_and_names))
#
# print(max(prices_and_names))

# prices = {'AAA': 45.23, 'ZZZ': 45.23}
# print(min(zip(prices.values(), prices.keys())))
# print(max(zip(prices.values(), prices.keys())))

# a = {
#     'x' : 1,
#     'y' : 2,
#     'z' : 3
# }
#
# b = {
#     'w': 10,
#     'x': 11,
#     'y': 2
# }
#
# print(a.items())  # items()方法返回包含(key, value)对的元素视图对象
# res1 = a.keys() & b.keys()  # 找相同的key
# print(res1)
# res2 = a.keys() - b.keys()  # 在a中不在b中的key
# print(res2)
# res3 = a.items() & b.items()  # 找到a b中相同的键值对
# print(res3)
#
# res4 = {key: a[key] for key in a.keys() - {'z'}}
# print(res4)
#
# a = [7, 8,1, 2, 3,4,5, 7,7 ,7, 8,2,1 ]
#
# l = set()
# for i in a:
#     if i in l:
#         pass
#     else:
#         l.add(i)
# print(l)

# items = [0, 1, 2, 3, 4, 5, 6]
# print(items[2: 6])
#
# slice_a = slice(2, 6)
#
# print(items[slice_a])
#
# print(type(slice_a))
#
# items[slice_a] = [7, 7, 7, 7, 7, 7]
# print(items)
#
# print(slice_a.start, slice_a.stop, slice_a.step)  # 切片各个属性
#
# slice_b = slice(5, 50, 2)
# print(slice_b.start, slice_b.stop, slice_b.step)

# slice_a = slice(2, 50, 2)
#
# print(slice_a)
# print(slice_a.indices(30))
#
# s = 'abcdefghijklmnopqrstuvwxyz'
#
# alp = []
# for i in range(*slice_a.indices(len(s))):
#     alp.append(s[i])
# print(alp)

# from collections import Counter
# words = [
#     'look', 'into', 'my', 'eyes', 'look', 'into', 'my', 'eyes',
#     'the', 'eyes', 'the', 'eyes', 'the', 'eyes', 'not', 'around', 'the',
#     'eyes', "don't", 'look', 'around', 'the', 'eyes', 'look', 'into',
#     'my', 'eyes', "you're", 'under'
# ]
#
# word_counts = Counter(words)
# print(word_counts) # 底层实现上一个Counter的对象相当于一个字典
# print(type(word_counts))
# print(word_counts['eyes'])
#
# top_three = word_counts.most_common(3)
# print(top_three)
#
# more_words = ['eyes', 'nose', 'eyes']
# word_counts.update(more_words)
# print(word_counts)
#
# word_counts['eyes'] += 1
# print(word_counts)

# from collections import Counter
#
# a = 'why are you so crazy?'
# b = 'I do not know.'
# count_a = Counter(a)
# count_b = Counter(b)
# print(count_a)
# print(count_b)
# print(count_a + count_b)
# print(count_a - count_b)


# class User:
#     def __init__(self, user_name, user_id):
#         self.user_name = user_name
#         self.user_id = user_id
#
#     def __repr__(self):
#         return 'User({}_{})'.format(self.user_name, self.user_id)
#
#
# users = [User('Jack', 12), User('Tom', 23), User('Harry', 32), User('Emma', 12)]
# print(users)
# # 方案一：lambda的方式
# print(sorted(users, key=lambda x: x.user_id))
#
# # 方案二：operator.attrgetter()的方式
# from operator import attrgetter
# print(sorted(users, key=attrgetter('user_id')))
# print(sorted(users, key=attrgetter('user_id', 'user_name')))
# print(min(users, key=attrgetter('user_id')))
# print(min(users, key=attrgetter('user_id', 'user_name')))
# print(max(users, key=attrgetter('user_id')))
#
# from itertools import groupby
# users = [User('Jack', 12), User('Tom', 32), User('Harry', 32), User('Emma', 12)]
# print(users.sort(key=attrgetter('user_id')))

# rows = [
#     {'address': '5412 N CLARK', 'date': '07/01/2012'},
#     {'address': '5148 N CLARK', 'date': '07/04/2012'},
#     {'address': '5800 E 58TH', 'date': '07/02/2012'},
#     {'address': '2122 N CLARK', 'date': '07/03/2012'},
#     {'address': '5645 N RAVENSWOOD', 'date': '07/02/2012'},
#     {'address': '1060 W ADDISON', 'date': '07/02/2012'},
#     {'address': '4801 N BROADWAY', 'date': '07/01/2012'},
#     {'address': '1039 W GRANVILLE', 'date': '07/04/2012'},
# ]
#
# from operator import itemgetter
# from itertools import groupby
#
# rows.sort(key=itemgetter('date'))
# print(rows)
#
# for data, items in groupby(rows, key=itemgetter('date')):
#     print(data)
#     for item in items:
#         print(item)

# import os
# import psutil
# pid = os.getpid()
# print(pid)
# a = ['a', 'b', 'c']
# for index, item in enumerate(a):
#     print(index, item)

# from itertools import zip_longest
# names = ['alpha', 'bate', 'delta', 'charlie']
# pnts = [23, 56, 32]
# for name, point in zip_longest(names, pnts):
#     print(name, point)
#
# print('==============')
#
# for name, point in zip_longest(names, pnts, fillvalue=0):
#     print(name, point)

# from itertools import *
# a = [1, 2, 3]
# b = set('alpha')
# c = {'a': 1, 'b': 2}
# for i in chain(a, b, c):
#     print(i)


# from collections.abc import Iterable
#
#
# def flatten(items, ignore_type=(str, bytes)):
#     for i in items:
#         if isinstance(i, Iterable) and not isinstance(i, ignore_type):  # isinstance(i, Iterable)检查元素是否可以迭代；
#             # not isinstance(i, ignore_type)将字符串和字节排除在可迭代对象外
#             yield from flatten(i)  # yield from在生成器中调用其他生成器作为子例程
#         else:
#             yield i
#
#
# sth = [1, 2, 3, [4, 5, [23, 12], 'jack'], [b'\x12\xff', 67]]
# for x in flatten(sth):
#     print(x)

# with open('sample.txt', 'wt') as f:
#     f.write('Hello World.\n')
#     f.write('Hello world again.\n')
#     f.write('Hello world the third time.')
#
# with open('sample.txt', 'rt') as f:
#     data = f.read()
#     print(data)
#
# with open('sample.txt', 'rt') as f:
#     for idx, line in enumerate(f):
#         print(idx, line)

#with open('sample.txt', 'at') as f:
#     print('print to file!', file=f)
# print('ACME', 50, 91.5)
# print('ACME', 50, 91.5, sep=',')
# print('ACME', 50, 91.5, sep=',', end='!\n')
#
# for i in range(5):
#     print(i)
#
# for i in range(5):
#     print(i, end=' ')  # 使用end参数也可以在输出中禁止换行
#
# row = ('ACME', 50, 91.5)
# print(row)
# print(*row, sep=',')

# with open('sample1.bin', 'wb') as f:
#
#     f.write(b'Hello wolrd')
#     f.write(b'\xcc\xdd\xff')
#
# with open('sample1.bin', 'rb') as f:
#     data = f.read()
#     print(data)
#     print(data.hex())

# text string 文本字符串
# t = 'Hello World'
# print(t[0])
# for i in t:
#     print(i, end=', ')
#
# print('\n========')
# Byte string 字节字符串
# t = b'Hello World'
# print(t.decode('utf-8'))
#
# t = 'Hello World'
# print(t.encode('utf-8'))

# print(t[0])
# for i in t:
#     print(i, end=', ')

# import array
# nums = array.array('i', [1, 2, 3, 4])
# with open('sample1.bin', 'xb') as f:
#     f.write(nums)

# with open('sample1.bin', 'rb') as f:
#     data = f.read()
#     print(data)
#     print(data.hex())

# with open('./files/file_1.txt') as f:
#     for line in f:
#         print(line)


import gzip
# from zipfile import ZipFile
# with ZipFile('./files/file_1.zip', 'r') as f:
#     with f.open('file_1.txt', 'r') as f1:
#         data = f1.read()
#         print(type(data))
#         print(data.decode())

# import os
#
#
# def read_into_buffer(filename):
#     buf = bytearray(os.path.getsize(filename))
#     with open(filename, 'rb') as f:
#         f.readinto(buf)
#     return buf
#
#
# with open(r'.\files\file_2.bin', 'wb') as f:
#     f.write(b'Hello World \xff')
# buf = read_into_buffer(r'.\files\file_2.bin')
# print(buf)
# import os
# names = os.listdir(r'D:\Codes\Learning_notes')
# print(names)
#
# file_names = [name for name in os.listdir(r'D:\Codes\Learning_notes')
#               if os.path.isfile(os.path.join(r'D:\Codes\Learning_notes', name))]
# print(file_names)
#
# dir_name = [name for name in os.listdir(r'D:\Codes\Learning_notes')
#             if os.path.isdir(os.path.join(r'D:\Codes\Learning_notes', name))]
# print(dir_name)

# from snapshot_selenium import snapshot
#
# # print(snapshot)
# import pyecharts.options as opts
# from pyecharts.charts import Grid, Boxplot, Scatter
# import pandas as pd
# import glob
# import time
# import os
# import operator
#
# path = r'\\172.16.2.20\qt\TestData\QT-128\4.版本测试\B sample\HB2第三轮迭代SOP\版本3.1.31测试数据\点云性能测试\定量测试\室内精准度测试\QT128C2X-C04-1190\高反板\QT128C2X-C04-1190_202302181019-15米'
#
# range_path = path + r'\*projection*.csv'
# range_path_list = glob.glob(range_path)
# datadic = {}
# for csv in range_path_list:
#     file_str = os.path.splitext(csv)[0]
#     laserid = file_str.split('_')[-1]
#     channelid = int(laserid) + 1
#     df = pd.read_csv(csv)
#     try:
#         distancelist = df.dis_projection.tolist()
#     except:
#         distancelist = []
#     datadic[channelid] = distancelist
#
# datadic = dict(sorted(datadic.items(), key=operator.itemgetter(0)))
# data_list = datadic.values()
# print(datadic)
#
# box_plot = Boxplot()
#
# box_plot = (
#     box_plot.add_xaxis(xaxis_data=[i for i in range(1, 129)])
#         .add_yaxis(series_name="", y_axis=box_plot.prepare_data(datadic.values()), )
#         .set_global_opts(
#         title_opts=opts.TitleOpts(
#             pos_left="center", title="Michelson-Morley Experiment"
#         ),
#         tooltip_opts=opts.TooltipOpts(trigger="item", axis_pointer_type="shadow"),
#     )
#     .render('velocity.html')
# )

# import plotly

# import plotly.express as px
# import pandas as pd
#
# dic = {'x': [1, 2, 3], 'y': [4, 5, 6], 'z': [7, 8, 9], 'ref': [23, 34, 65], 'conf': [1, 0, 1]}
#
# df = pd.DataFrame(dic)
# fig = px.scatter_3d(df, x='x', y='y', z='z',
#                     color='ref', symbol='conf')
# fig.write_html('sam.html')
# print('lllll')

# a = 0
# try:
#     while True:
#         print(a)
#         assert a < 5
#         a += 1
#         print(a, 'OK')
# except Exception as e:
#     print(str(e))
# #
# # print('done')
# # from graphics.primitive.text import *
# # spam()
#
#
# # from graphics.primitive.text import *
# # spam()
# # grok()
# import numpy as np
# from scipy.optimize import curve_fit
# import matplotlib.pyplot as plt
#
# # 假设有一组数据
# x_data = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
# y_data = np.array([0, 2, 8, 18, 30, 45, 60, 42, 20, 5])
#
# # 定义高斯函数
# def gaussian(x, A, mu, sigma):
#     return A * np.exp(-(x - mu)**2 / (2 * sigma**2))
#
# # 使用curve_fit函数进行高斯拟合
# params, covariance = curve_fit(gaussian, x_data, y_data, p0=[1, np.mean(x_data), 1])
#
# # 获取拟合参数
# A, mu, sigma = params
#
# # 绘制拟合曲线
# x_fit = np.linspace(0, 9, 100)  # 创建用于绘制拟合曲线的x值
# y_fit = gaussian(x_fit, A, mu, sigma)
#
# # 绘制原始数据和拟合曲线
# plt.plot(x_data, y_data, 'bo', label='Data')
# plt.plot(x_fit, y_fit, 'r-', label='Fit')
# plt.legend()
# plt.show()
#
# # 输出拟合参数
# print(f'A = {A}, mu = {mu}, sigma = {sigma}')

# import pandas as pd
#
# # 创建一个示例DataFrame
# data = {'A': [1, 2, 3, 4, 5],
#         'B': [10, 20, 30, 40, 50]}
#
# df = pd.DataFrame(data)
#
# # 使用条件判断创建新列
# df['new_column'] = 0  # 先初始化新列
#
# # 基于条件判断给新列赋值
# df['new_column'] = df.apply(lambda row: row['A'] if row['A'] > 3 else row['B'] - 1, axis=1)
#
# print(df)
from hashlib import sha256
import pandas as pd
import numpy as np
import os

# def angle_bin_file_gen(sn, angle_df_path, save_path):
#     """
#     生成角度文件bin文件
#
#     :return:
#     """
#     header = [0xee, 0xff, 0x04, 0x01, 0x00, 0x00, 0x30]
#
#     df = pd.read_csv(angle_df_path)
#     print(df)
#     angle_list = df['Azimuth'].tolist() + df['Elevation'].tolist()
#     angle_int_list = [int(i * (2 ** 9)) for i in angle_list]
#
#     data = header + [512] + angle_int_list
#     print(data)
#
#     d = struct.pack('<7BH96h', *data)
#     sha = sha256(d).hexdigest()
#     save_bin = os.path.join(save_path, '{}_calibration.dat'.format(sn))
#
#     file = open(save_bin, 'wb')
#     file.write(d)
#     file.write(bytes.fromhex(sha))
#     print('Transition Done.')
#
#
#
# angle_bin_file_gen('0006', r'D:\WORK\MT\MT5_A0_Calibration\0006_Angular_test_202310282008\0006_calibration.csv', r'D:\WORK\MT\MT5_A0_Calibration\0006_Angular_test_202310282008')

# with open(r'D:\WORK\MT\MT5_A0_Calibration\0010_Angular_test_202310282206\0010_calibration.dat', 'rb') as file_handle:
#     data = file_handle.read()
# print(data.hex())
# print(len(data))

# df = pd.read_csv(r'D:\WORK\MT\参数2文件\006\0006_calibration.csv')
#
# df2 = pd.DataFrame({'LaserID': df.LaserID.tolist(),
#                     'Azimuth': [i - 5 for i in df.Azimuth.tolist()],
#                     'Elevation': df.Elevation.tolist()})
# df2.to_csv(r'D:\WORK\MT\参数2文件\006\0006_calibration1.csv', index=None)

# a = 4.096
# b = a * 512
# c = int(b)
# print(c)
# d = c.to_bytes(2, 'big', signed=True)
# print(d.hex())

# b = b'\xfe\x24'
# value = int.from_bytes(b, byteorder='big', signed=False)
#
# print(value/512)
#
# import pandas as pd
#
# # 创建一个示例DataFrame
# data = {'列1': [10, 15, 30, 25],
#         '列2': [5, 12, 20, 18],
#         '列3': [8, 14, 28, 24]}
# df = pd.DataFrame(data)
#
# # 定义要进行加法操作的列名列表
#
#
# # 针对每一列，将其加上20
#
# df['列1'] = df['列1'] + 20
#
# # 打印结果
# print(df)
#
# a = -0.1
# a_int = int(0.128 * 512)
# print(a_int)
# print(a_int.to_bytes(2, 'big').hex())

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# excel_file_path = r'D:\WORK\MT\1107AngleCalib\A0-012_Angular_test_202311072121\elevation\1_angle_ele.xlsx'
# sheet_name = 'Sheet1'
# columns_to_read = ['angle', 'intens']
# df = pd.read_excel(excel_file_path, sheet_name=sheet_name, usecols=columns_to_read)
# print(df)
#
# def gaussian(x, amplitude, mean, stddev):
#     return amplitude * np.exp(-((x - mean) / stddev) ** 2 / 2)
#
#
# # 生成示例数据
# x_data = np.array(df['angle'].tolist())  # 输入数据
# y_data = np.array(df['intens'].tolist())  # 对应的输出数据
#
# # 初始猜测参数
# initial_guess = [max(y_data), np.mean(x_data), np.std(x_data)]
#
# # 进行高斯拟合
# params, covariance = curve_fit(gaussian, x_data, y_data, p0=initial_guess)
#
# # 提取拟合后的参数
# amplitude, mean, stddev = params
#
# # 绘制原始数据和拟合结果
# plt.plot(x_data, y_data, 'bo', label='Original Data')
# plt.plot(x_data, gaussian(x_data, amplitude, mean, stddev), 'r-', label='Fit')
#
# # 显示峰值
# peak_value = gaussian(mean, amplitude, mean, stddev)
# print("峰值:", peak_value)
# print("峰值对应的自变量:", mean)
#
# # 显示图例和绘制图形
# plt.legend()
# plt.show()
# from PIL import Image, ImageDraw, ImageFont
#
# def modify_letter(input_path, output_path, target_letter, new_letter):
#     # 打开图像
#     image = Image.open(input_path)
#
#     # 获取图像的宽度和高度
#     width, height = image.size
#
#     # 创建一个用于绘制文本的ImageDraw对象
#     draw = ImageDraw.Draw(image)
#
#     # 选择字体和字号
#     font = ImageFont.load_default()
#
#     # 遍历图像的每个像素
#     for x in range(width):
#         for y in range(height):
#             # 获取当前像素的颜色值
#             current_color = image.getpixel((x, y))
#
#             # 获取当前像素的字母
#             current_letter = chr(current_color[0])
#
#             # 如果当前像素的字母是目标字母，则替换为新字母
#             if current_letter == target_letter:
#                 draw.text((x, y), new_letter, font=font, fill=current_color)
#
#     # 保存修改后的图像
#     image.save(output_path)
#
# # 示例用法
# modify_letter(r"\\10.69.31.10\ft\专项测试\客户Mobis测试\20231201_C-final雷达室内测远能力\RangeTest_FT120-C-final-C051_202312011926-22.764m\FT120-C-final-C051_result_at_22.764.png",
#               r"C:\Users\wanghaibo\Downloads\output.png", "u", "e")


import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.font_manager import FontProperties
#
# # 设置中文字体
# plt.rc('font', family='Time New Rome')
# plt.rcParams['font.family'] = 'simhei'
# plt.rcParams['axes.unicode_minus'] = False
#
#
# df = pd.read_csv(r'\\10.69.31.10\ft\版本测试\FT120 SOP版本测试\20231129_室外测远\FT120-PV-0003\10m\RangeTest_FT120-PV-0003_202311281540\FT120-PV-0003_result_at_10.253.csv')
#
# # 创建一个7行10列的文本数据
#
# # 创建图表
# fig, ax = plt.subplots()
# plt.xlim(-1, 11)
# plt.ylim(-1, 10)
#
# # 在图上添加文本
# for i in range(10):
#     for j in range(7):
#         ax.text(i, 9 - j, 'Area {}\n\n POD: {}'.format(j * 10 + i, df['POD'].tolist()[j * 10 + i]), ha="center", va="center", fontsize=10)
# plt.title('FT120 全区域探测概率 10%@10m (100klx)', fontsize=25)
# # 显示图表
# plt.show()

# df = pd.read_csv(r'C:\Users\wanghaibo\Downloads\MT_A1_a1.csv')
#
# df_re = pd.DataFrame({'Laser ID': df['CH'].tolist(),
#                       'Azimuth': [-i for i in df['水平视场角/°'].tolist()],
#                       'Elevation': df['垂直视场角/°'].tolist()})
# df_re.to_csv(r'C:\Users\wanghaibo\Downloads\MT_A1_a1_mirror.csv', index=False)
# print(df_re)
# i = 0
# store = []
# for _ in range(5):
#     i += 1
#     store.add(i)
#     print(i)
# print(store)
# import os
#
# os.add_dll_directory('D:\WORK\FT\时间戳规律')

# import pandas as pd

# 创建一个示例DataFrame
# data = {
#     'A': [1, 2, 3, 1, 2],
#     'B': ['a', 'b', 'c', 'a', 'b'],
#     'C': ['x', 'y', 'z', 'x', 'y']
# }
# df = pd.DataFrame(data)
#
# # 指定'A'列和'B'列的数据相同时删除重复行
# result_df = df.drop_duplicates(subset=['A', 'B'])
#
# print("Original DataFrame:")
# print(df)
# print("\nDataFrame after dropping duplicates:")
# print(result_df)

#
# import pandas as pd
#
# # 创建一个示例DataFrame
# data = {
#     'x': [0.467816, 0.467484, 0.467711, 0.466618, 0.467345, 0.466717, 0.467171, 0.465955],
#     'y': [-107.214790, -107.138870, -107.190811, -106.940201, -107.106903, -106.963051, -107.066940, -106.788330],
#     'z': [4.906145, 4.902670, 4.905047, 4.407377, 4.901207, 4.894625, 4.899379, 4.401118],
#     'azimuth': [179.75, 179.75, 179.75, 179.75, 179.75, 179.75, 179.75, 179.75],
#     'elevation': [0.045728, 0.045728, 0.045728, 0.041190, 0.045728, 0.045728, 0.045728, 0.041190]
# }
# df = pd.DataFrame(data)
#
# # 指定前两列的数据相同时删除重复行
# result_df = df.drop_duplicates(subset=['azimuth', 'elevation'])
# #
# # print("Original DataFrame:")
# # print(df)
# # print("\nDataFrame after dropping duplicates based on 'x' and 'y' columns:")
# # print(result_df)
#
# import open3d as o3d
# import numpy as np
#
# # 读取PCD文件为点云数据
# pcd_path = r'D:\WORK\Benchmarking\HW96\range\130\1.pcd'
# point_cloud = o3d.io.read_point_cloud(pcd_path)
#
# # 将点云数据转换为NumPy数组
# points = np.asarray(point_cloud.points)
#
# print("NumPy array of points:")
# print(points)
#
# import pyttsx3
#
# # 创建一个语音引擎
# engine = pyttsx3.init()
#
# # 设置你想要的语音速度（默认为200）
# engine.setProperty('rate', 150)  # 150 words per minute
#
# # 设置你想要的语音音量（范围从0到1）
# engine.setProperty('volume', 0.9)  # 90% volume
#
# # 将文本转换为语音
# text = "Welcome to Sigma Lab. 欢迎来到西格玛实验室。"
# engine.say(text)
#
# # 等待语音播放完毕
# engine.runAndWait()

# import numpy as np
#
# # 示例1: 计算单个点的角度
# y = 1
# x = 1
# angle = np.arctan2(y, x)
# print(f"Angle for point (1, 1): {angle} radians, {np.degrees(angle)} degrees")
#
# # 示例2: 计算多个点的角度
# y = np.array([0, 1, 1, -1, -1])
# x = np.array([1, 1, -1, -1, 1])
# angles = np.arctan2(y, x)
# print(f"Angles in radians: {angles}")
# print(f"Angles in degrees: {np.degrees(angles)}")
#
# # 示例3: 使用广播机制计算标量和数组之间的角度
# y = np.array([1, 2, 3])
# x = 1
# angles = np.arctan2(y, x)
# print(f"Angles for points (1,1), (2,1), (3,1): {angles} radians, {np.degrees(angles)} degrees")

#
# from scapy.all import *
# from collections import defaultdict
#
# def reassemble_ip_fragments(pcap_file):
#     packets = rdpcap(pcap_file)
#     fragments = defaultdict(list)
#     reassembled_packets = []
#
#     # Collect all fragments by (src_ip, dst_ip, id)
#     for packet in packets:
#         if IP in packet:
#             ip_layer = packet[IP]
#             if ip_layer.frag != 0 or ip_layer.flags & 1:  # Check if the packet is fragmented
#                 key = (ip_layer.src, ip_layer.dst, ip_layer.id)
#                 fragments[key].append(ip_layer)
#
#     # Reassemble the fragments
#     for key, fragment_list in fragments.items():
#         if fragment_list:
#             fragment_list.sort(key=lambda x: x.frag)
#             reassembled_data = b""
#             for fragment in fragment_list:
#                 reassembled_data += bytes(fragment.payload)
#             reassembled_packets.append(reassembled_data)
#
#     return reassembled_packets
#
#
# # Example usage
# pcap_file = r'D:\WORK\Benchmarking\Robin_W\robin_a.pcap'
# reassembled_data_list = reassemble_ip_fragments(pcap_file)
# for data in reassembled_data_list:
#     print(data)

# import socket
# import select
#
#
# def clear_buffer(sock):
#     """
#     清除套接字缓冲区中的数据。重点在于使用select.select进行非阻塞检查，如果没有可读数据则跳出循环，实现清空缓存的作用。
#     :param sock:
#     :return:
#     """
#     sockets = [sock]  # 将套接字放入一个列表中，因为select函数需要一个列表作为输入。
#     while True:
#         inputready, _, _ = select.select(sockets, [], [], 0.0)
#         # select.select函数用于监视sockets列表中的套接字，检查是否有可读数据。
#         # 第一个参数：检查可读性的套接字列表；第二个参数：检查可写性的套接字列表；第三个参数：检查异常状态的套接字列表；第四个参数：超时时间，0.0表示立即返回，不等待
#         print(inputready)
#         if not inputready:
#             break
#         for s in inputready:
#             try:
#                 s.recv(2048)
#             except Exception as e:
#                 print('清除缓冲区时出错：{}'.format(e))
#                 return
#
#
# udpsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# udpsock.bind(('', 2368))
# udpsock.settimeout(10)
#
# clear_buffer(udpsock)


# my_list = [1, 2, 2, 3, 4, 4, 5]
# unique_list = list(set(my_list))
# print(unique_list)
#
# my_list = [1, 2, 2, 3, 4, 4, 5]
# unique_list = list(dict.fromkeys(my_list))
# print(unique_list)
#
# from collections import Counter
#
# my_list = [1, 2, 2, 3, 4, 4, 5]
# count_dict = dict(Counter(my_list))
# print(count_dict)
#
# int.from_bytes()

# print('fad gjkhsg'.split())

import turtle

# def draw_spiral(my_turtle, line_len):
#     if line_len > 0:
#         my_turtle.forward(line_len)
#         my_turtle.right(90)
#         draw_spiral(my_turtle, line_len - 5)
#
# my_turtle = turtle.Turtle()
# my_win = turtle.Screen()
# draw_spiral(my_turtle, 100)
# my_win.exitonclick()

# def tree(branch_len, t):
#     if branch_len > 5:
#         t.forward(branch_len)
#         t.right(20)
#         tree(branch_len - 15, t)
#
#         t.left(40)
#         tree(branch_len - 15, t)
#         t.right(20)
#         t.backward(branch_len)
#
# t = turtle.Turtle()
# my_win = turtle.Screen()
# t.left(90)
# t.up()
# t.backward(200)
# t.down()
# t.color('red')
# tree(110, t)
# my_win.exitonclick()

# def sum_add(num_list):
#     if len(num_list) == 1:
#         return num_list[0]
#
#     else:
#         print(sum_add(num_list[1:]) + num_list[0])
#         return sum_add(num_list[1:]) + num_list[0]
#
# sum_add([1, 2, 3, 4])

#
def draw_branch(branch_length):
    # 绘制分形树
    if branch_length > 5:
        # 绘制右侧树枝
        turtle.forward(branch_length)
        print('向前', branch_length)
        turtle.right(20)
        print('右转 20')
        draw_branch(branch_length - 15)

        # 绘制左侧树枝
        turtle.left(40)
        print('左转 40')
        draw_branch(branch_length - 15)

        # 返回之前的树枝
        turtle.right(20)
        print('右转 20')
        print(branch_length)
        turtle.backward(branch_length)
        print('向后', branch_length)



# 图形设置
turtle.left(90)
turtle.penup()
turtle.backward(260)
turtle.pendown()
turtle.pensize(1)
turtle.pencolor('red')

# 调用递归函数
draw_branch(120)
turtle.exitonclick()

# def get_raio(x, up_value):
#     y1 = (1.53184 - 1.07499) / 99 * (x - 1) + 1.0749
#     y2 = (1.53184 - 0.4) / 99 * (x - 1) + 0.4
#     return up_value * (y2 / y1)
#
#
# import pandas as pd
# import matplotlib.pyplot as plt
# import matplotlib.font_manager as fm
# # 设置中文字体，确保系统中安装了黑体字体
# plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
# plt.rcParams['axes.unicode_minus'] = False    # 解决坐标轴负号显示问题
#
# file_path = r'C:\Users\wanghaibo\Downloads\artificial sun\101spectra.xlsx'
#
# df = pd.read_excel(file_path, sheet_name='567')
#
# row_index = 9
#
# row_data = df.iloc[row_index]
# row_list = row_data.tolist()[1:]
# rate1 = 1.53184 / row_list[-1]
#
# fuzhaodu = [i * rate1 for i in row_list]
# adjust_list = [get_raio(i+1, fuzhaodu[i]) for i in range(100)]
# print(fuzhaodu)
# print(adjust_list)
#
# plt.scatter([i for i in range(1, 101)], adjust_list, marker='o')
# plt.title('点光源905nm辐照度与功率比例关系')
# plt.xlabel('点光源功率比例(%)')  # 横坐标标签
# plt.ylabel('辐照度(W/m^2/nm)')  # 纵坐标标签
# plt.show()
#
# ditc = {
#     'light_rate(%)': [i for i in range(1, 101)],
#     '辐照度':adjust_list
# }
#
# pd.DataFrame(ditc).to_csv(r'C:\Users\wanghaibo\Downloads\artificial905.csv')