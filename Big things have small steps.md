### unique()
pandas中Series获取唯一值的方法（去除重复项）：

unique()方法

Example:
```python
import pandas as pd
dic = {'a': [1, 2, 3, 3, 3, 2, 2, 4],
       'b': [2, 2, 2, 2, 2, 2, 2, 2]}
df = pd.DataFrame(dic)
print(df)
unil = df.a.unique().tolist()
print(unil)
"""
   a  b
0  1  2
1  2  2
2  3  2
3  3  2
4  3  2
5  2  2
6  2  2
7  4  2
[1, 2, 3, 4]
"""
```
### DataFrame的自动补齐功能（broadcast？）
可以用来构造DataFrame
```python
import pandas as pd
result = pd.DataFrame({'laser_id': [i for i in range(1, 9)], 
					   'accuracy': 0, 
                       'precision': 0, 
                       'RMSE': 0,
                       'thick': 0,
                       'points_count': 0, 
                       'frames': 0,
                       'POD': 0})
print(result)

"""
   laser_id  accuracy  precision  RMSE  thick  points_count  frames  POD
0         1         0          0     0      0             0       0    0
1         2         0          0     0      0             0       0    0
2         3         0          0     0      0             0       0    0
3         4         0          0     0      0             0       0    0
4         5         0          0     0      0             0       0    0
5         6         0          0     0      0             0       0    0
6         7         0          0     0      0             0       0    0
7         8         0          0     0      0             0       0    0
"""
```
### os.makedirs()
创建文件夹
```python
import os
path = r'D:/files'
if not (os.path.exists(path)):   # 取反判断，如果path不存在文件夹，则新建。os.path.exist返回布尔值。
	os.makedirs(path)
```

### 字典get()方法
Python 字典 get() 函数返回指定键的值
```python
dic = {'a': [1, 2, 3, 4],
       'b': [5, 6, 7, 8]}
p = dic.get('a')
print(p)

"""
[1, 2, 3, 4]
"""
```

### with open() as f
```python
with open(r'filename.txt') as f:
   data_user=pd.read_csv(f)  #文件的读操作

with open('data.txt', 'w') as f:
   f.write('hello world')  #文件的写操作

"""
r:	以只读方式打开文件。文件的指针将会放在文件的开头。这是**默认模式**。
rb: 以二进制格式打开一个文件用于只读。文件指针将会放在文件的开头。这是默认模式。
r+: 打开一个文件用于读写。文件指针将会放在文件的开头。
rb+:以二进制格式打开一个文件用于读写。文件指针将会放在文件的开头。
w:	打开一个文件只用于写入。如果该文件已存在则将其覆盖。如果该文件不存在，创建新文件。
wb:	以二进制格式打开一个文件只用于写入。如果该文件已存在则将其覆盖。如果该文件不存在，创建新文件。
w+:	打开一个文件用于读写。如果该文件已存在则将其覆盖。如果该文件不存在，创建新文件。
wb+:以二进制格式打开一个文件用于读写。如果该文件已存在则将其覆盖。如果该文件不存在，创建新文件。
a:	打开一个文件用于追加。如果该文件已存在，文件指针将会放在文件的结尾。也就是说，新的内容将会被写入到已有内容之后。如果该文件不存在，创建新文件进行写入。
ab:	以二进制格式打开一个文件用于追加。如果该文件已存在，文件指针将会放在文件的结尾。也就是说，新的内容将会被写入到已有内容之后。如果该文件不存在，创建新文件进行写入。
a+:	打开一个文件用于读写。如果该文件已存在，文件指针将会放在文件的结尾。文件打开时会是追加模式。如果该文件不存在，创建新文件用于读写。
ab+:以二进制格式打开一个文件用于追加。如果该文件已存在，文件指针将会放在文件的结尾。如果该文件不存在，创建新文件用于读写。
"""
```
file对象的属性
```python
file.read([size])   将文件数据作为字符串返回，可选参数size控制读取的字节数
file.readlines([size])   返回文件中行内容的列表，size参数可选
file.write(str)   将字符串写入文件
file.writelines(strings)   将字符串序列写入文件
file.close()   关闭文件
file.closed	表示文件已经被关闭，否则为False

file.mode	Access文件打开时使用的访问模式
file.encoding	文件所使用的编码
file.name	文件名
file.newlines	未读取到行分隔符时为None，只有一种行分隔符时为一个字符串，当文件有多种类型的行结束符时，则为一个包含所有当前所遇到的行结束的列表
file.softspace	为0表示在输出一数据后，要加上一个空格符，1表示不加。这个属性一般程序员用不着，由程序内部使用
```
### time.time()
多用于计算两个时间点之间的间隔
```python
import time
t1 = time.time()  # 返回当前时间的时间戳（1970纪元后经过的浮点秒数）。
t2 = time.localtime(t1)  # 分别是年、月、日、时、分、秒、星期（一周第几天）、天数（一年第几天）、是否为夏令时（1）
t3 = time.asctime(t2)
print(t1)
print(t2)
print(t3)

"""
1607341602.9163291
time.struct_time(tm_year=2020, tm_mon=12, tm_mday=7, tm_hour=19, tm_min=46, tm_sec=42, tm_wday=0, tm_yday=342, tm_isdst=0)
Mon Dec  7 19:46:42 2020
"""
```
### 向csv文件追加写入数据
```python
df_data.to_csv('data.csv', mode='a', header=True, index=False

"""
mode='a'：即向csv文件追加数据，按行追加（如果不存在这个 csv文件，则创建一个并 添加数据）
header=True：写入dataframe的列名（表头）
index=False：不添加索引列
"""
```
### concat() 
```python
pd.concat(objs, axis=0, join='outer', join_axes=None, ignore_index=False)
"""
objs: Series, DataFrame等
axis: 需要合并连接的轴，0是行，1是列
join： 连接的方式inner， 或者outer
"""
```
相同字段首尾连接
```python
import numpy as np
import pandas as pd
df1 = pd.DataFrame(np.arange(6).reshape(2, 3), columns=['a', 'b', 'c'])
df2 = pd.DataFrame(np.arange(6, 12).reshape(2, 3), columns=['a', 'b', 'c'])
df3 = pd.DataFrame(np.arange(12, 18).reshape(2, 3), columns=['a', 'b', 'c'])
dflist = [df1, df2, df3]
df_s = pd.concat(dflist)
print(df1)
print(df2)
print(df3)
print(df_s)

"""
   a  b  c
0  0  1  2
1  3  4  5

   a   b   c
0  6   7   8
1  9  10  11

    a   b   c
0  12  13  14
1  15  16  17

    a   b   c
0   0   1   2
1   3   4   5
0   6   7   8
1   9  10  11
0  12  13  14
1  15  16  17
"""
```
### GIL 全局解释器锁
GIL 是最流程的 CPython 解释器（平常称为 Python）中的一个技术术语，中文译为全局解释器锁，其本质上类似操作系统的 Mutex。GIL 的功能是：在 CPython 解释器中执行的每一个 Python 线程，都会先锁住自己，以阻止别的线程执行。

当然，CPython 不可能容忍一个线程一直独占解释器，它会轮流执行 Python 线程。这样一来，用户看到的就是“伪”并行，即 Python 线程在交替执行，来模拟真正并行的线程。
```python
from _datetime import datetime
start = datetime.now()
def countdown(n):
    while n > 0:
        n -= 1
countdown(100000)
print("Time used:", (datetime.now() - start))
"""
Time used: 0:00:00.006981
"""
```
```python
from datetime import datetime
from threading import Thread
start = datetime.now()
def CountDown(n):
    while n > 0:
        n -= 1
t1 = Thread(target=CountDown, args=[100000 // 2])
t2 = Thread(target=CountDown, args=[100000 // 2])
t1.start()
t2.start()
t1.join()
t2.join()
print("Time used:", (datetime.now() - start))
"""
Time used: 0:00:00.007985
"""
```

### ininstance()函数
isinstance()函数来判断一个对象是否是一个已知的类型
#### 语法
```python
isinstance(object, classinfo)
```
#### 参数
 - object 实例对象
 - classinfo 可以是直接或间接类名、基本类型或者有它们组成的元组
#### 返回值
如果对象的类型与参数二的类型（classinfo）相同则返回True，否则返回False
```python
a = 2.3
r1 = isinstance(a, int)
r2 = isinstance(a, float)
r3 = isinstance(a, (str, float, list))
print(r1, r2, r3)
"""d
False True True
"""
```