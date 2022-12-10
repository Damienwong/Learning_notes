# 查找最大or最小的N个元素

### 简单list
```python
import heapq
nums = [21, 34, 0.2, -4, -5, 3, 1, 100, 100]
print(heapq.nlargest(3, nums))
print(heapq.nsmallest(4, nums))


"""
[100, 100, 34]
[-5, -4, 0.2, 1]
"""
```

### 复杂数据结构
```python
import heapq
portfolio = [
    {'name': 'IBM', 'shares': 100, 'price': 91.1},
    {'name': 'AAPL', 'shares': 50, 'price': 543.22},
    {'name': 'FB', 'shares': 200, 'price': 21.09},
    {'name': 'HPQ', 'shares': 35, 'price': 31.75},
    {'name': 'YHOO', 'shares': 45, 'price': 16.35},
    {'name': 'ACME', 'shares': 75, 'price': 115.65}
]
cheap = heapq.nsmallest(3, portfolio, key=lambda s: s['price'])
expensive = heapq.nlargest(3, portfolio, key=lambda s: s['price'])
print(cheap)
print(expensive)

"""
[{'name': 'YHOO', 'shares': 45, 'price': 16.35}, {'name': 'FB', 'shares': 200, 'price': 21.09}, {'name': 'HPQ', 'shares': 35, 'price': 31.75}]
[{'name': 'AAPL', 'shares': 50, 'price': 543.22}, {'name': 'ACME', 'shares': 75, 'price': 115.65}, {'name': 'IBM', 'shares': 100, 'price': 91.1}]
"""
```

### 模块的底层实现是先将集合数据进行堆排序后放入一个列表中
堆排列的定义：
https://blog.csdn.net/weixin_51609435/article/details/122982075
```python
nums = [1, 8, 2, 23, 7, -4, 18, 23, 42, 37, 2]
import heapq
heapq.heapify(nums)
print(nums)

"""
[-4, 2, 1, 23, 7, 2, 18, 23, 42, 37, 8]
"""
```

### heapq.heappoq()获取最小值并弹出
```python
nums = [1, 8, 2, 23, 7, -4, 18, 23, 42, 37, 2]
import heapq
heapq.heapify(nums)
print(nums)
# 查找最小的3个函数
print(heapq.heappop(nums))
print(heapq.heappop(nums))
print(heapq.heappop(nums))

"""
[-4, 2, 1, 23, 7, 2, 18, 23, 42, 37, 8]
-4
1
2
"""
```

