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

string1 = 'aabbcc0102ff'
bits = bytes.fromhex(string1)  # 字符串转化为字节流
print(type(bits), bits)

string2 = bits.hex()  # 字节流转化为字符串
print(type(string2), string2)

# string3 = str(bits)
# print(type(string3), string3)
# struct.unpack('6B', string3)
