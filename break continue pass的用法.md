### break,continue,pass,else的用法

break: 结束整个循环过程，包含for循环和while循环，**只能跳出当前层次的循环（最内层）**

continue: 结束当前**当次**循环，即跳出本次循环中还没有执行的语句，并不跳出当前整个循环

pass: 不做任何作用，只起到占位的作用，不会跳出循环

```python
for i in "python":
    if i == "t":
        continue
    print(i, end="")

"""
pyhon
"""
```

```python
for i in "python":
    if i == "t":
        break
    print(i, end="")

"""
py
"""
```

```python
for i in "python":
    if i == "t":
        pass
    print(i, end="")

"""
python
"""
```

### else在for循环和while循环中的扩展用法

else中的程序在：

1、正常循环循环结束后执行，包含continue

2、在因break和return而结果的循环后**不执行**

```python
for i in "python":
    if i == "t":
        continue
    print(i, end="")
else:
    print("程序正常退出")

"""
pyhon程序正常退出
"""
```

```python
for i in "python":
    if i == "t":
        break
    print(i, end="")
else:
    print("程序正常退出")

"""
py
"""
```