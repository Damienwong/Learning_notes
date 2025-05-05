# -*- coding: utf-8 -*-
# @Time     : 2023/4/19 19:31
# @Author   : WHB
# @File     : process_test
# @Software : PyCharm

import multiprocessing as mp
import time
from rclpy.node import Node

def process_1(process_alive,receive_start,data_queue):

    process_alive.wait() # 等待事件触发,process_alive 被set后执行下面的函数

    while process_alive.is_set():

        receive_start.wait() # 等待 进程2 给指令
        while receive_start.is_set():
            # do something
            r_time = time.time()
            # print("process_1",r_time)
            time.sleep(2) # 这边模拟收2s的包；收的时间要比处理时间长，不然一个周期内就会收到太多次数据，会比较不好处理
            r_time2 = time.time()
            print("process_1发送的数据", r_time2)
            if not receive_start.is_set():
                break
            data_queue.put(r_time2)
            # print(r_time2)
            break

        receive_start.wait()

        #做完了,那就置为等待

def process_2(process_alive,receive_start,data_queue):

    process_alive.wait()  # 等待事件触发,process_alive 被set后执行下面的函数

    while process_alive.is_set():

        #do something
        for i in range(5):
            receive_start.set()

            while data_queue.empty(): # receive_start信号触发了，需要在这里等待 形式可以是：进程1传递一些东西过来；如果不等待的话， 进程2就一直干自己的事，一直重复set\clear receive_start，那么进程1可能来不及做
                time.sleep(0.001)
            # do something
            d_time = data_queue.get()
            print("process_2收到的数据",i,d_time)
            # do something  处理逻辑之类的
            receive_start.clear()
            # time.sleep(2)
        # 循环都做完了，process_alive 置为false

        process_alive.clear()

def run():
    #主进程
    data_queue = mp.Queue() # 在两个进程之间用于共享数据的队列
    process_alive = mp.Event() # 事件：用于run主函数 控制两个子进程的 状态
    receive_start = mp.Event() # 事件：用于进程2 控制进程1的；比如进程2为处理数据进程，1为收包进程；

    p_1 = mp.Process(target=process_1,args=(process_alive,receive_start,data_queue)) # 这里还可以放其他的参数 比如 共享数据的队列data_queue等等
    p_2 = mp.Process(target=process_2,args=(process_alive,receive_start,data_queue))

    p_1.start()
    p_2.start()

    process_alive.set() #  控制两个进程开启

    while process_alive.is_set():
        time.sleep(1)
    # 两个进程一直存活期间，主进程可以在这里等待，也可以做其他事

    # process_alive 可以是在子进程内 状态被置为false,则表示子进程内要做的事做完了，告诉run主进程将子进程结束

    # join函数让主进程等待子进程结束之后，再执行主进程。
    p_1.terminate()
    p_1.join()
    p_2.terminate()
    p_2.join()

if __name__ == '__main__':
    run()