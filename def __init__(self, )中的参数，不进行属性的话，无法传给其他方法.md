```python
class Test():
    def __init__(self, para):
        self.para = para

    def test_it(self):
        print(para)  # para无法传递给该方法

if __name__ == "__main__":
    t = Test(3)
    t.test_it()
    
"""
NameError: name 'para' is not defined
"""
```