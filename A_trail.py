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

s1 = '{:#08x}'.format(15)
s2 = '{:#8x}'.format(15)

s3 = '0x{:08x}'.format(15)
s4 = '0x{:8x}'.format(15)

print(' s1: {}\n'.format(s1),
      's2: {}\n'.format(s2),
      's3: {}\n'.format(s3),
      's4: {}\n'.format(s4))
