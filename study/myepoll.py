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
		print('some event runing...')
		for fileno,event in events:
			print('句柄+事件,%s:%s' % (fileno,event))
			if fileno == ser.fileno():
				'''
				客户端加入
				'''
				print('new cli add')
				cli,addr = ser.accept()
				cli.setblocking(False)
				cli_no = cli.fileno()
				#epoll_loop.register(cli_no,select.EPOLLIN|select.EPOLLET)
				epoll_loop.register(cli_no,select.EPOLLIN)
				conns[fileno] = cli
				request[cli_no] = b''
			elif event & EPOLLIN:
				print('cli data input')
				try:
					request[fileno] += conns[fileno].recv(100) 
					if not request[fileno]:
						raise ConnectionRestError('没有数据')
				except ConnectionRestError:
					'''
					客户端关闭
					'''
					epoll_loop.unregister(fileno)
					conns[fileno].close()
					request.remove(fileno)
					if response[fileno]:
						response.remove(fileno) 
			elif event & EPOLLOUT:
				print('cli data output')
				try:
					ret = conns[fileno].sendall(request[fileno])
					if ret != None:
						raise KeyError('服务端响应数据失败')
				except ConnectionRestError:
					'''
					客户端关闭
					'''
					epoll_loop.unregister(fileno)
					conns[fileno].close()
					request.remove(fileno)
					if response[fileno]:
						response.remove(fileno) 
				except KeyError:
					continue
			elif event & EPOLLHUP:
				epoll_loop.unregister(fileno)
				conns[fileno].close()
				request.remove(fileno)
				if response[fileno]:
					response.remove(fileno) 
finally:
	print('closing all')
	epoll_loop.unregister(ser.fileno())
	epoll_loop.close()
	ser.close()
				
			
			
		