import socket

udp = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
udp.bind(('',9090))
string = '1:14524125:XXX:XXX:32:你好啊!'
udp.sendto(string.encode('gbk'),('11.129.129.135',2425))
recver , dst_ip = udp.recvfrom(1024)
print(recver.decode('gbk',errors='ignore'),dst_ip)
