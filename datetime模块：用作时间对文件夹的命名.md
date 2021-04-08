可以获取当前时间，或者用作对结果文件存放位置的命名
```python
from datetime import datetime
print(datetime.now())
a = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 注意：month和day是小写，大写M是分钟（minute），大写的D是整体日期（date）。
b = datetime.now().__str__()
print(a)
print(b)
```
打印结果

```python
2020-10-13 18:28:00.344154
2020-10-13 18:28:00
2020-10-13 18:28:00.344154
```
