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

from collections import Counter

a = 'why are you so crazy?'
b = 'I do not know.'
count_a = Counter(a)
count_b = Counter(b)
print(count_a)
print(count_b)
print(count_a + count_b)
print(count_a - count_b)



