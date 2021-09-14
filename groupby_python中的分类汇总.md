```python
import pandas as pd
all_info = {'azimuth': [1, 1, 2, 3, 3, 1, 1, 2, 2, 3, 2],
            'distance_m': [1., 1.1, 2., 3.3, 3., 1.1, 1.1, 2.2, 2.2, 3.3, 2.2]}

a_pd = pd.DataFrame(all_info)
a_pd = a_pd.loc[(a_pd['distance_m'] > 0)]
new_pd = a_pd.groupby('azimuth').agg('min')  # 参数可以是'mean'/'min'/'max'/'sum'等，类似于Excel中的数据透视表
new_df = new_pd.reset_index()
print(new_df)

"""
   azimuth  distance_m
0        1       1.075
1        2       2.150
2        3       3.200
"""
```