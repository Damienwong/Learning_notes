```python
import xlrd
data = xlrd.open_workbook(file)  #读取Excel内容，放入变量data中
table = data.sheet_by_index(0)  #获取第0个sheet
lens = table.nrows  #获取表格的行数
sn_list = table.col_values(0)  #获取第0列，返回列表
sn = table.col_values(0)[1]  #获取第0列的第1行
ip = table.col_values(1)[1]  #获取第1列的第1行
```
