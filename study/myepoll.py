import socket
import select 

ip = ('127.0.0.1',9999)
ser = socket.socket()
ser.setblocking(False)
ser.bind(ip)
ser.listen(10)
print('server:%s' % ser)
epoll_loop = select.epoll() 
epoll_loop.register(ser.fileno(),select.EPOLLIN)
try:
	conns = {}
	request = {}
	response = {}
	while True:
		events = epoll_loop.poll(1)
		for fileno,event in events:
			print('句柄+事件,%s:%s' % (fileno,event))
			if fileno == ser.fileno():
				'''
				客户端加入
				'''
				cli,addr = ser.accept()
				cli.setblocking(False)
				epoll_loop.
				conns[fileno] = cli
				
				
			
			
		