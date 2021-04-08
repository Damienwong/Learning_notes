## DataFrame中的apply函数和lambda
#### apply
#### apply函数主要用于对DataFrame中的行或者列进行特定的函数计算。
apply(func [, args [, kwargs]])函数用于当函数参数已经存在于一个元组或者字典中（DataFrame）时，间接的调用函数。
```python
import pandas as pd
import numpy as np
dic = {'A': [1, 1, 1, 1],
       'B': [12, 15, 34, 98],
       'C': [45, 23, 88, 23]}
df = pd.DataFrame(dic)
result1 = df.apply(np.mean)  # 默认axis=0, 遍历每一行的数据（即计算每列的平均值）
result2 = df.apply(np.mean, axis=1)  # 遍历每一列的数据（即计算每行的平均值）
print(df)
print(result1)
print(result2)

"""
   A   B   C
0  1  12  45
1  1  15  23
2  1  34  88
3  1  98  23

A     1.00
B    39.75
C    44.75
dtype: float64

0    19.333333
1    13.000000
2    41.000000
3    40.666667
dtype: float64
"""
```
#### lambda
lambda是匿名函数，即不再使用def的形式来定义函数，可以简化脚本。
```python
a = lambda x : x + 1
print(a(10))

"""
11
"""
```
### apply + lambda可以实现很多NB的事情
```python
import pandas as pd

# 先生成一个dataframe
d = {"col1": ["96%(1368608/1412722)",
              "97%(1389916/1427922)",
              "97%(1338695/1373803)",
              "96%(1691941/1745196)",
              "95%(1878802/1971608)",
              "97%(944218/968845)",
              "96%(1294939/1336576)"]}
df1 = pd.DataFrame(d)

# 切分原文中识别率总数，采用apply + 匿名函数
# lambda 函数的意思是选取x的序列值 ，比如 x[6:9]
# index函数的意思是把当前字符位置转变为所在位置的位数
# -1是最后一位
df1['正确数'] = df1.iloc[:, 0].apply(lambda x: x[x.index('(') + 1: x.index('/')])
df1['总数'] = df1.iloc[:, 0].apply(lambda x: x[x.index('/') + 1: -1])
df1['正确率'] = df1.iloc[:, 0].apply(lambda x: x[:x.index('(')])
print(df1)

"""
               col1      正确数       总数  正确率
0  96%(1368608/1412722)  1368608  1412722  96%
1  97%(1389916/1427922)  1389916  1427922  97%
2  97%(1338695/1373803)  1338695  1373803  97%
3  96%(1691941/1745196)  1691941  1745196  96%
4  95%(1878802/1971608)  1878802  1971608  95%
5    97%(944218/968845)   944218   968845  97%
6  96%(1294939/1336576)  1294939  1336576  96%
"""

```