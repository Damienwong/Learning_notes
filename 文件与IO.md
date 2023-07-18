# 文件与IO

## 1. 文本数据

```python
with open('sample.txt', 'wt') as f:   # 'xt',可以防止文件被覆盖，文件不存在才会创建。存在则报错。
    f.write('Hello World.\n')
    f.write('Hello world again.\n')
    f.write('Hello world the third time.')

with open('sample.txt', 'rt') as f:
    data = f.read()
    print(data)

with open('sample.txt', 'rt') as f:
    for idx, line in enumerate(f):
        print(idx, line)


"""
Hello World.
Hello world again.
Hello world the third time.
0 Hello World.

1 Hello world again.

2 Hello world the third time.
"""
```

## 2. 打印至文件中
```python
with open('sample.txt', 'at') as f:
    print('print to file!', file=f)
```

## 3. 打印技巧
```python
print('ACME', 50, 91.5)
print('ACME', 50, 91.5, sep=',')
print('ACME', 50, 91.5, sep=',', end='!\n')

for i in range(5):
    print(i)

for i in range(5):
    print(i, end=' ')  # 使用end参数也可以在输出中禁止换行

row = ('ACME', 50, 91.5)
print(row)
print(*row, sep=',')

"""
ACME 50 91.5
ACME,50,91.5
ACME,50,91.5!
0
1
2
3
4
0 1 2 3 4 ('ACME', 50, 91.5)
ACME,50,91.5
"""
```

## 4.二进制文件
```python
with open('sample1.bin', 'wb') as f:
    f.write(b'Hello wolrd')
    f.write(b'\xcc\xdd\xff')

with open('sample1.bin', 'rb') as f:
    data = f.read()
    print(data)
    print(data.hex())

# text string 文本字符串
t = 'Hello World'
print(t[0])
for i in t:
    print(i, end=', ')

print('\n========')
# Byte string 字节字符串
t = b'Hello World \xff'
print(t[0])
for i in t:
    print(i, end=', ')
    
'''
b'Hello wolrd\xcc\xdd\xff'
48656c6c6f20776f6c7264ccddff
H
H, e, l, l, o,  , W, o, r, l, d, 
========
72
72, 101, 108, 108, 111, 32, 87, 111, 114, 108, 100, 32, 255, 
'''
```

## 5.打开压缩文件
```python
from zipfile import ZipFile
with ZipFile('./files/file_1.zip', 'r') as f:
    with f.open('file_1.txt', 'r') as f1:
        data = f1.read()
        print(type(data))
        print(data.decode())

"""
<class 'bytes'>
Hello World
Hello World again
"""
```

## 6.读取二进制数据到可变缓冲区
```python
import os


def read_into_buffer(filename):
    buf = bytearray(os.path.getsize(filename))
    with open(filename, 'rb') as f:
        f.readinto(buf)
    return buf


with open(r'.\files\file_2.bin', 'wb') as f:
    f.write(b'Hello World \xff')
buf = read_into_buffer(r'.\files\file_2.bin')
print(buf)

"""
bytearray(b'Hello World \xff')
"""
```

## 7.获取文件夹文件列表
```python
import os
names = os.listdir(r'D:\Codes\Learning_notes')
print(names)

file_names = [name for name in os.listdir(r'D:\Codes\Learning_notes')
              if os.path.isfile(os.path.join(r'D:\Codes\Learning_notes', name))]
print(file_names)

dir_name = [name for name in os.listdir(r'D:\Codes\Learning_notes')
            if os.path.isdir(os.path.join(r'D:\Codes\Learning_notes', name))]
print(dir_name)

"""
[' zip创建多序列迭代器.md', '.git', '.idea', '.ipynb_checkpoints', '.numpy模块_2', '.strip()方法.md', '.TCP_IP_Learning_notes_2', 'Arduino', 'A_trail.py', 'Big things have small steps.md', 'break continue pass的用法.md', 'CGI_sample.py', 'CRC32.py', 'datetime模块：用作时间对文件夹的命名.md', 'def __init__(self, )中的参数，不进行属性的话，无法传给其他方法.md', 'files', 'groupby_python中的分类汇总.md', 'Ideas and Plans.md', 'ImagesFolder', 'matplotlib的boxplot上画真值横线.md', 'multiprocessing模块 Process和Queue.md', 'numpy模块.md', 'pandas DataFrame中的apply函数和lambda函数.md', 'Pcap文件的N中解析方式.md', 'Pcap文件的数据结构.md', 'PTC_sample.py', 'pyechart', 'pyinstaller打包exe.md', 'Python_Cookbook', 'Python代码中的一些注意格式.md', 'Python按位运算.md', 'Readme.md', 'sample.txt', 'sample1.bin', 'sklearn.linear_model.LinearRefression最小二乘法线性回归.md', 'socket模块.md', 'struct.unpack带符号的整型解析.md', 'tcpdump.md', 'TCP_IP_Learning_notes.md', 'temp.md', 'things be noted.md', 'xlrd模块读取Excel中的数据.md', '切片的命名.md', '字典的聚类和排序.md', '字典的计算.md', '字符串、字节流、整数转化.md', '对字典进行排序并返回字典，key或者value.md', '小端对齐和大端对齐.md', '展开嵌套的序列.md', '文件与IO.md', '类属性的排序.md', '计数器collections.Counter.md', '雷达中的坐标系：x, y, z和distance、elevation、azimuth_calib的关系.md']
[' zip创建多序列迭代器.md', '.strip()方法.md', 'A_trail.py', 'Big things have small steps.md', 'break continue pass的用法.md', 'CGI_sample.py', 'CRC32.py', 'datetime模块：用作时间对文件夹的命名.md', 'def __init__(self, )中的参数，不进行属性的话，无法传给其他方法.md', 'groupby_python中的分类汇总.md', 'Ideas and Plans.md', 'matplotlib的boxplot上画真值横线.md', 'multiprocessing模块 Process和Queue.md', 'numpy模块.md', 'pandas DataFrame中的apply函数和lambda函数.md', 'Pcap文件的N中解析方式.md', 'Pcap文件的数据结构.md', 'PTC_sample.py', 'pyinstaller打包exe.md', 'Python代码中的一些注意格式.md', 'Python按位运算.md', 'Readme.md', 'sample.txt', 'sample1.bin', 'sklearn.linear_model.LinearRefression最小二乘法线性回归.md', 'socket模块.md', 'struct.unpack带符号的整型解析.md', 'tcpdump.md', 'TCP_IP_Learning_notes.md', 'temp.md', 'things be noted.md', 'xlrd模块读取Excel中的数据.md', '切片的命名.md', '字典的聚类和排序.md', '字典的计算.md', '字符串、字节流、整数转化.md', '对字典进行排序并返回字典，key或者value.md', '小端对齐和大端对齐.md', '展开嵌套的序列.md', '文件与IO.md', '类属性的排序.md', '计数器collections.Counter.md', '雷达中的坐标系：x, y, z和distance、elevation、azimuth_calib的关系.md']
['.git', '.idea', '.ipynb_checkpoints', '.numpy模块_2', '.TCP_IP_Learning_notes_2', 'Arduino', 'files', 'ImagesFolder', 'pyechart', 'Python_Cookbook']
"""

```

