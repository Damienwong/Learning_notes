# Python计数的类collections.Counter

```python
from collections import Counter
words = [
    'look', 'into', 'my', 'eyes', 'look', 'into', 'my', 'eyes',
    'the', 'eyes', 'the', 'eyes', 'the', 'eyes', 'not', 'around', 'the',
    'eyes', "don't", 'look', 'around', 'the', 'eyes', 'look', 'into',
    'my', 'eyes', "you're", 'under'
]

word_counts = Counter(words)
print(word_counts) # 底层实现上一个Counter的对象相当于一个字典
print(type(word_counts))
print(word_counts['eyes'])

top_three = word_counts.most_common(3)
print(top_three)

more_words = ['eyes', 'nose', 'eyes']
word_counts.update(more_words)  # 在原有对象的基础上增加
print(word_counts)

word_counts['eyes'] += 1
print(word_counts)

"""
Counter({'eyes': 8, 'the': 5, 'look': 4, 'into': 3, 'my': 3, 'around': 2, 'not': 1, "don't": 1, "you're": 1, 'under': 1})
<class 'collections.Counter'>
8
[('eyes', 8), ('the', 5), ('look', 4)]
Counter({'eyes': 10, 'the': 5, 'look': 4, 'into': 3, 'my': 3, 'around': 2, 'not': 1, "don't": 1, "you're": 1, 'under': 1, 'nose': 1})
Counter({'eyes': 11, 'the': 5, 'look': 4, 'into': 3, 'my': 3, 'around': 2, 'not': 1, "don't": 1, "you're": 1, 'under': 1, 'nose': 1})
"""
```

## Counter实例的数学运算
```python
from collections import Counter

a = 'why are you so crazy?'
b = 'I do not know.'
count_a = Counter(a)
count_b = Counter(b)
print(count_a)
print(count_b)
print(count_a + count_b)
print(count_a - count_b)

"""
Counter({' ': 4, 'y': 3, 'a': 2, 'r': 2, 'o': 2, 'w': 1, 'h': 1, 'e': 1, 'u': 1, 's': 1, 'c': 1, 'z': 1, '?': 1})
Counter({' ': 3, 'o': 3, 'n': 2, 'I': 1, 'd': 1, 't': 1, 'k': 1, 'w': 1, '.': 1})
Counter({' ': 7, 'o': 5, 'y': 3, 'w': 2, 'a': 2, 'r': 2, 'n': 2, 'h': 1, 'e': 1, 'u': 1, 's': 1, 'c': 1, 'z': 1, '?': 1, 'I': 1, 'd': 1, 't': 1, 'k': 1, '.': 1})
Counter({'y': 3, 'a': 2, 'r': 2, 'h': 1, ' ': 1, 'e': 1, 'u': 1, 's': 1, 'c': 1, 'z': 1, '?': 1})
"""
```