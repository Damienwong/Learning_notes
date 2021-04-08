![雷达为中心的坐标系](https://img-blog.csdnimg.cn/20201020161830282.jpg?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80NDY5NDc5OQ==,size_6,color_FFFFFF,t_70#pic_center)
雷达的坐标系，x指向码盘的90度方向，y指向码盘的0度方向。
#### 与distance_m、elevation、azimuth_calib的关系。
$x = distance\_m \times cos(elevation) \times sin(azimuth\_calib)$
$y = distance\_m \times cos(elevation) \times cos(azimuth\_calib)$ 
$z = distance\_m \times sin(elevation)$

![在这里插入图片描述](https://img-blog.csdnimg.cn/20201020162746760.PNG?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80NDY5NDc5OQ==,size_16,color_FFFFFF,t_70#pic_center)
```python
import numpy as np
z = 4.756 * np.sin(np.radians(21.415))
x = 4.756 * np.cos(np.radians(21.415)) * np.sin(np.radians(24.460))
y = 4.756 * np.cos(np.radians(21.415)) * np.cos(np.radians(24.460))
print(x, y, z)

'''
1.8333020782645435 4.030268153896452 1.7365132010782374
'''
```