雷达复用字段存在温度为负的情况，因此采用有符号整型数据记录。

例如：复用字段为：
```python
bits = b'\x4f\xfc\x0a'
```


ID = 11 为RX温度

小端对齐解析前两位：
```python
import struct
bits = b'\x4f\xfc\x0a'
RX_temp = struct.unpack('<h',bits[0:2])  # h表示带符号的整型
RX_temp = RX_temp[0]/100
print(RX_temp)

"""
结果：
-9.45
"""
```

手撸结果：
(fc4f)H =(1111 1100 0100 1111)B  这是补码

转化为原码为：1000 0011 1011 0001

该原码计算为十进制的结果是：945

![](.struct.unpack带符号的整型解析_images/4920824b.png)
![](.struct.unpack带符号的整型解析_images/c6454533.png)


