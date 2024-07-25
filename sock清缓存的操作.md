# socket清缓存的操作

```python
import socket
import select


def clear_buffer(sock):
    """
    清除套接字缓冲区中的数据。重点在于使用select.select进行非阻塞检查，如果没有可读数据则跳出循环，实现清空缓存的作用。
    :param sock:
    :return:
    """
    sockets = [sock]  # 将套接字放入一个列表中，因为select函数需要一个列表作为输入。
    while True:
        inputready, _, _ = select.select(sockets, [], [], 0.0)
        # select.select函数用于监视sockets列表中的套接字，检查是否有可读数据。
        # 第一个参数：检查可读性的套接字列表；第二个参数：检查可写性的套接字列表；第三个参数：检查异常状态的套接字列表；第四个参数：超时时间，0.0表示立即返回，不等待
        print(inputready)
        if not inputready:
            break
        for s in inputready:
            try:
                s.recv(2048)
            except Exception as e:
                print('清除缓冲区时出错：{}'.format(e))
                return


udpsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udpsock.bind(('', 2368))
udpsock.settimeout(10)

clear_buffer(udpsock)
```