import socket
import select 

ip = ('127.0.0.1',9999)
ser = socket.socket()
ser.setblocking(False)
ser.bind(ip)
ser.listen(10)
print('server:%s' % ser,',no:',ser.fileno())
epoll_loop = select.epoll() 
epoll_loop.register(ser.fileno(),select.EPOLLIN)
try:
	conns = {}
	request = {}
	response = {}
	while True:
		events = epoll_loop.poll(10)
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
				conns[cli_no] = cli
				request[cli_no] = b''
			elif event & select.EPOLLIN:
				print('cli data input')
				try:
					request[fileno] += conns[fileno].recv(100) 
					epoll_loop.register(fileno,select.EPOLLOUT)
					if not request[fileno]:
						raise ConnectionResetError('没有数据')
				except ConnectionResetError:
					'''
					客户端关闭
					'''
					print('cli %s close' % fileno)
					epoll_loop.unregister(fileno)
					conns[fileno].close()
					request.pop(fileno)
					if fileno in response:
						response.pop(fileno) 
			elif event & select.EPOLLOUT:
				print('cli data output')
				try:
					ret = conns[fileno].sendall(request[fileno])
					if ret != None:
						raise KeyError('服务端响应数据失败')
				except ConnectionResetError:
					'''
					客户端关闭
					'''
					print('cli %s close' % fileno)
					epoll_loop.unregister(fileno)
					conns[fileno].close()
					request.pop(fileno)
					if fileno in response:
						response.pop(fileno) 
				except KeyError:
					continue
			elif event & select.EPOLLHUP:
				epoll_loop.unregister(fileno)
				conns[fileno].close()
				request.pop(fileno)
				if fileno in response:
					response.pop(fileno) 
finally:
	print('closing all')
	epoll_loop.unregister(ser.fileno())
	epoll_loop.close()
	ser.close()
				
			
			
		