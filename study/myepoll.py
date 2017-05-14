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
				cli,addr = ser.accept()
				cli.setblocking(False)
				cli_no = cli.fileno()
				print('new cli add:%s' % cli_no)
				#epoll_loop.register(cli_no,select.EPOLLIN|select.EPOLLET)
				epoll_loop.register(cli_no,select.EPOLLIN)
				conns[cli_no] = cli
				request[cli_no] = b''
			elif event & select.EPOLLIN:
				print('cli data input:%s' % fileno)
				try:
					request[fileno] += conns[fileno].recv(10) 	
					print('%s:%s,data:%s' %(fileno,conns[fileno].recv(100),request[fileno]))
					if not request[fileno]:
						raise ConnectionResetError('没有数据')
					epoll_loop.modify(fileno,select.EPOLLOUT)
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
				try:
					ret = conns[fileno].sendall(request[fileno])
					print('cli data output:%s,data:%s,ret:%s' % (fileno,request[fileno],ret))
					if ret != None:
						raise KeyError('服务端响应数据失败')
					else:
						epoll_loop.modify(fileno,select.EPOLLIN)
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
				print('cli hup:%s' % fileno)
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
				
			
			
		