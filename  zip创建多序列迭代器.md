## 同时迭代多个序列

zip(a, b)会生成一个可返回元组(x, y)的迭代器，其中x来自a，y来自b，一旦某个序列到底结束，迭代结束。

因此迭代长度更参数中最短序列长度一致。

```python
names = ['alpha', 'bate', 'delta', 'charlie']
pnts = [23, 56, 32, 67]
for name, point in zip(names, pnts):
    print(name, point)

"""
alpha 23
bate 56
delta 32
charlie 67
"""
```

```python
names = ['alpha', 'bate', 'delta', 'charlie']
pnts = [23, 56, 32]
for name, point in zip(names, pnts):
    print(name, point)

'''
alpha 23
bate 56
delta 32
'''
```

如果想要保留较长的序列，可用用itertools.zip_longest()函数来实现

```python
from itertools import zip_longest
names = ['alpha', 'bate', 'delta', 'charlie']
pnts = [23, 56, 32]
for name, point in zip_longest(names, pnts):
    print(name, point)

print('==============')

for name, point in zip_longest(names, pnts, fillvalue=0):
    print(name, point)

"""
alpha 23
bate 56
delta 32
charlie None
==============
alpha 23
bate 56
delta 32
charlie 0
"""
```