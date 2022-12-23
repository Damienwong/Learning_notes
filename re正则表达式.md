# re正则表达式

https://docs.python.org/zh-cn/3/library/re.html?highlight=re%20split#re.split
### 多个界定符分割字符串
```python
import re
line = 'asdf fjdk; afed, fjek,asdf, foo'
str_list = re.split(r'[;,\s]\s*', line)
print(str_list)

"""
['asdf', 'fjdk', 'afed', 'fjek', 'asdf', 'foo']
"""
```

上述用到的正则表达式的语法：
```python
[] # 表示一个字符集合：1、单独列出，[amk]匹配'a', 'm' 或者 ‘k'
   # 2、表示字符范围[a-z]表示所有小写ASCII字符
\s # 对于str,匹配任何Unicode空白字符，包括[\t\n\r\f\v]
*  # 对它前面的正则式匹配0到任意次重复。ab*会匹配到a b 或者a后面跟随任意个b。上述\s*表示可以跟任意个空白字符。
```