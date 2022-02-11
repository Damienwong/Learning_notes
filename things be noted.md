## 打开linux串口权限
```commandline
cd /dev
ls -l | grep USB
sudo chmod 777 /dev/ttyUSB0
```

## 查看及修改电脑缓存空间大小
```commandline
history | grep rmem_default
cat /proc/sys/net/core/rmem_default  #看缓存空间大小
sysctl -w net.core.rmem_default=26214400  #设置缓存空间大小
```