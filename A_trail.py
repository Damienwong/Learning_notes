# -*- coding: utf-8 -*-

# a = 2.3
# r1 = isinstance(a, int)
# r2 = isinstance(a, float)
# r3 = isinstance(a, (str, float, list))
# print(r1, r2, r3)

import struct
bits = b'\x4f\xfc\x0a'
RX_temp = struct.unpack('<h',bits[0:2])
RX_temp = RX_temp[0]/100
print(RX_temp)

