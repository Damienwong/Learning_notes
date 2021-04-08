如果字典的key时可排序的数值，可以对字典进行排序，并将结果返回给字典。
```python
import operator
dic = {3: 1, 2: 23, 1: 17}
sort_key_dic = dict(sorted(dic.items(), key=operator.itemgetter(0)))  #按照key值升序
sort_val_dic = dict(sorted(dic.items(), key=operator.itemgetter(1)))  #按照value值升序
print(sort_key_dic)  # output:{1: 17, 2: 23, 3: 1}
print(sort_val_dic)  # output:{3: 1, 1: 17, 2: 23}
```
打印结果：

```python
{1: 17, 2: 23, 3: 1}
{3: 1, 1: 17, 2: 23}
```