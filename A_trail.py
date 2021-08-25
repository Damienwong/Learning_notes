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

print(hex(255))
print(b'\xff'.hex())