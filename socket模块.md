### 1.socket
socket.socket()函数创建套接字：
socket.socket(socket_family, socket_type, protocol=0)
socket_family可以是如下参数：
 - AF_INET 指IPv4(默认)
 - AF_INET6 指IPv6
 - AF_UNIX 只能够用于单一的Unix系统进程间通信
 
socket_type可以是如下参数：
 - SOCK_STREAM  流式socket，for TCP（默认）
 - SOCK_DGRAM 数据报式socket，for UDP
 - SOCK_RAW 原始套接字，普通的套接字无法处理ICMP、IGMP等网络报文，而SOCK_RAW可以；其次，SOCK_RAW也可以处理特殊的IPv4报文；此外，利用原始套接字，可以通过IP_HDRINCL套接字选项由用户构造IP头。
 - SOCK_RDM 是一种可靠的UDP形式，即保证交付数据报但不保证顺序。SOCK_RAM用来提供对原始协议的低级访问，在需要执行某些特殊操作时使用，如发送ICMP报文。SOCK_RAM通常仅限于高级用户或管理员运行的程序使用。
 - SOCK_SEQPACKET 可靠的连续数据包服务。

protocol参数：
0 （默认）与特定的地址家族相关的协议，如果是0，则系统就会根据地址格式和套接类别，自动选择一个合适的协议。
