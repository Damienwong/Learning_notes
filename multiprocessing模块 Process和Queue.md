# Multiprocessing 模块
## 管理进程模块

 - Process（用于创建进程模块）
 - Pool（用于创建管理进程池）
 - Queue（用于进程通信，资源共享）
 - Value， Array（用于进程通信，资源共享）
 - Pipe（用于管道通信）
 - Manager（用于资源共享）
 
## 子进程（Process）
 ```python
 Process(group=None, target=None, name=None, args=(), kwargs={}, *, deamon=None)
 # group为预留参数
 # target为可调用对象（函数对象），为子进程对应的活动
 # name为线程的名称，默认（None）是‘Process-N’
 # args, kwargs为进程活动（target）的非关键字参数、关键字参数
 # deamon为bool值，表示是否为守护进程。
 ```
 - run()
表示进程运行的方法。可以在子类中重写此方法。标准run() 方法调用传递给对象构造函数的可调用对象作为目标参数（如果有），分别使用args和kwargs参数中的顺序和关键字参数。
 - start（）
进程准备就绪，等待CPU调度。
 - join（[ 超时] ）
       如果可选参数timeout是None，则该方法将阻塞，直到join()调用其方法的进程终止。如果timeout是一个正数，它最多会阻塞超时秒。请注意，None如果方法的进程终止或方法超时，则返回该方法。检查进程exitcode以确定它是否终止。
 - name
进程的名称。该名称是一个字符串，仅用于识别目的。
 - is_alive（）
返回进程是否存活。从start() 方法返回到子进程终止的那一刻，进程对象仍处于活动状态。
 - daemon
进程的守护进程标志，一个布尔值。必须在start()调用之前设置，当进程退出时，它会尝试终止其所有守护进程子进程。
 - pid
返回进程ID。在产生该过程之前，这将是 None。
 - exitcode
子进程的退出代码。None如果流程尚未终止，这将是。负值-N表示孩子被信号N终止。
```python
from multiprocessing import Process
import time
import os

def info():
    print('module name:', __name__)
    print('parent process:', os.getppid())
    print('process id:', os.getpid())

def f(name):
    info()
    time.sleep(3)
    print('hello', name)

if __name__ == '__main__':
    info()
    p = Process(target=f, args=('bob',))
    # p.daemon = False
    print(p.daemon)
    p.start()
    p.join(1)
    print('name:', p.name)
    print('is_alive:', p.is_alive())
    print('exitcode:', p.exitcode)
'''
------------------------------------------------------------
module name: __main__
parent process: 1188
process id: 13060
False
module name: __mp_main__
parent process: 13060
process id: 13424
name: Process-1
is_alive: True
exitcode: None
hello bob
------------------------------------------------------------
'''
```
在上述逻辑中，子进程会休息3s然后再打印一句话才结束，同时设定join(1)阻塞1s，阻塞在1s后结束，我们的并没有守护主进程，然后主进程结束后，子进程依然alive。

如果想要守护主进程，设定p.daemon = True
```python
if __name__ == '__main__':
    info()
    p = Process(target=f, args=('bob',))
    p.daemon = True
    print(p.daemon)
    p.start()
    # p.join(1)
    print('name:', p.name)
    print('is_alive:', p.is_alive())
    print('exitcode:', p.exitcode)
'''
------------------------------------------------------------
module name: __main__
parent process: 1188
process id: 1668
True
name: Process-1
is_alive: True
exitcode: None
------------------------------------------------------------
'''
```
在上述逻辑中，子进程会休息3s然后再打印一句话才结束，我们的设定守护主进程，然后主进程结束后，打印的is_alive: True这句话其实是在主进程里运行的，所以此时子进程确实是alive，但是主进程结束后子进程也结束了，不会运行info() 函数。

## 队列（Queue）
### 概念----multiProcess.Queue
创建共享的进程队列，Queue是多进程安全的队列，可以使用Queue*****实现多进程之间的数据传递*****。

`Queue([maxsize])`创建共享的进程队列。

参数 ：maxsize是队列中允许的最大项数。如果省略此参数，则无大小限制。

```python
from multiprocessing import Queue
q = Queue()  #生成一个队列对象
```
当使用多个进程时，通常使用消息传递来进行进程之间的通信。对于传递消息，可以使用**队列Queue（允许多个生产者和消费者）。**
##### Queue用来在多个进程间通信。Queue有两个方法，get和put：

 - put：放数据
 Queue.put()默认有block=True和timeout两个参数。当block=True时，写入是阻塞式的，阻塞时间由timeout确定。当队列q被（其他线程）写满后，这段代码就会阻塞，直至其他线程取走数据。Queue.put（）方法加上 block=False 的参数，即可解决这个隐蔽的问题。但要注意，非阻塞方式写队列，当队列满时会抛出 exception Queue.Full 的异常。
 - get：取数据（默认阻塞）
 Queue.get([block[, timeout]])获取队列，timeout等待时间
```python
from multiprocessing import Process, Queue
import os, time, random


# 写数据进程执行的代码:
def _write(q,urls):
    print('Process(%s) is writing...' % os.getpid())
    for url in urls:
        q.put(url)
        print('Put %s to queue...' % url)
        time.sleep(random.random())


# 读数据进程执行的代码:
def _read(q):
    print('Process(%s) is reading...' % os.getpid())
    while True:
        url = q.get(True)
        print('Get %s from queue.' % url)


if __name__=='__main__':
    # 父进程创建Queue，并传给各个子进程：
    q = Queue()
    _writer1 = Process(target=_write, args=(q,['url_1', 'url_2', 'url_3']))
    _writer2 = Process(target=_write, args=(q,['url_4','url_5','url_6']))
    _reader = Process(target=_read, args=(q,))
    # 启动子进程_writer，写入:
    _writer1.start()
    _writer2.start()
    # 启动子进程_reader，读取:
    _reader.start()
    # 等待_writer结束:
    _writer1.join()
    _writer2.join()
    # _reader进程里是死循环，无法等待其结束，只能强行终止:
    _reader.terminate()

"""
Process(15448) is reading...
Process(5444) is writing...
Put url_4 to queue...
Get url_4 from queue.
Process(6140) is writing...
Put url_1 to queue...
Get url_1 from queue.
Put url_5 to queue...
Get url_5 from queue.
Put url_6 to queue...
Get url_6 from queue.
Put url_2 to queue...
Get url_2 from queue.
Put url_3 to queue...
Get url_3 from queue.
"""
```
##### put_nowait 与 get_nowait
put与get方法是两个阻塞方法：put不到值程序夯住，get不到程序也夯住。
put_nowait与get_nowait方法是两个非阻塞方法：put_nowait没有值的话不等，get_nowait取不到值也不等了，程序不会夯住，但是一定要做异常处理！
```python
from multiprocessing import Queue

# 只能放我5个
q = Queue(5)
q.put(1)
q.put(2)
q.put(3)
q.put(4)
q.put(5)
print('******')
q.put(6)
print('######')

print(q.get())
print(q.get())
print(q.get())
print(q.get())
print(q.get())
print(q.get())

"""
******    #程序夯住（卡死）
"""
```
因为在创建Queue的对象时规定最多只能放5个，如果多放的话程序会夯在第6个位置。
如果想要放数据的话，可以在第6个位置用put_nowait方法。
```python
from multiprocessing import Queue

# 只能放我5个
q = Queue(5)
q.put(1)
q.put(2)
q.put(3)
q.put(4)
q.put(5)
print('******')
q.put_nowait(6)
print('######')

print(q.get())
print(q.get())
print(q.get())
print(q.get())
print(q.get())
print(q.get())

"""
******
Traceback (most recent call last):
  File "D:/Coding/for_trial_only/test1/test.py", line 27, in <module>
    q.put_nowait(6)
  File "C:\Users\wanghaibo\AppData\Local\Programs\Python\Python37\lib\multiprocessing\queues.py", line 129, in put_nowait
    return self.put(obj, False)
  File "C:\Users\wanghaibo\AppData\Local\Programs\Python\Python37\lib\multiprocessing\queues.py", line 83, in put
    raise Full
queue.Full
"""
```
multiprocessing使用通常queue.Empty和 queue.Full异常来发出超时信号。它们在multiprocessing命名空间中不可用，因此需要从中导入它们 queue。
```python
import queue
from multiprocessing import Queue

# 只能放我5个
q = Queue(5)
q.put(1)
q.put(2)
q.put(3)
q.put(4)
q.put(5)
print('******')
try:
    q.put_nowait(6)
    print('######')
except queue.Full:
    print('队列溢出，做点别的处理')
    pass

print(q.get())
print(q.get())
print(q.get())
print(q.get())
print(q.get())
print(q.get())

"""
******
队列溢出，做点别的处理
1
2
3
4
5
"""
```
可以看到：没有进行异常里面的内容~~没有打印‘’######‘可以看到。

但是！注意了！我明明用了6个get，但结果只有五个数！第6个get不到数据，程序夯住。

因此：put_nowait方法会丢失数据！当然我们可以把丢失的数据放在别的文件或其他数据结构中，但是，这样不常用，因此实际情况下**put_nowait不常用**！

加上异常处理：
```python
import queue
from multiprocessing import Queue

# 只能放我5个
q = Queue(5)
q.put(1)
q.put(2)
q.put(3)
q.put(4)
q.put(5)
print('******')
try:
    # 满了的话我也不等
    q.put_nowait(6)
    print('######')
except queue.Full:
    print('队列溢出，做点别的处理')
    pass

print(q.get())
print(q.get())
print(q.get())
print(q.get())
print(q.get())
try:
    # 空了的话数据我就不取了
    print(q.get_nowait())
except queue.Empty:
    pass
```