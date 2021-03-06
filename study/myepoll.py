import socket
import select 

ip = ('127.0.0.1',9999)
ser = socket.socket()
ser.setblocking(False)
ser.bind(ip)
ser.listen(10)
'''
EPOLLIN	Available for read
EPOLLOUT	Available for write
EPOLLPRI	Urgent data for read
EPOLLERR	Error condition happened on the assoc. fd
EPOLLHUP	Hang up happened on the assoc. fd
EPOLLET	Set Edge Trigger behavior, the default is Level Trigger behavior
EPOLLONESHOT	Set one-shot behavior. After one event is pulled out, the fd is internally disabled
EPOLLRDNORM	Equivalent to EPOLLIN
EPOLLRDBAND	Priority data band can be read.
EPOLLWRNORM	Equivalent to EPOLLOUT
EPOLLWRBAND	Priority data may be written.
EPOLLMSG	Ignored.
'''
print(select.EPOLLIN)
print(select.EPOLLOUT)
print(select.EPOLLPRI)
print(select.EPOLLERR)
print(select.EPOLLHUP)
print(select.EPOLLET)
print(select.EPOLLONESHOT)
print(select.EPOLLRDNORM)
print(select.EPOLLRDBAND)
print(select.EPOLLWRNORM)
print(select.EPOLLWRBAND)
print(select.EPOLLMSG)
print('server:%s' % ser,',no:',ser.fileno())
print('in:%s,out:%s,hup:%s,et:%s' %(select.EPOLLIN,select.EPOLLOUT,select.EPOLLHUP,select.EPOLLET))
epoll_loop = select.epoll() 
epoll_loop.register(ser.fileno(),select.EPOLLIN)
try:
	conns = {}
	request = {}
	response = {}
	while True:
		events = epoll_loop.poll(100)
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
				print(event,'&',select.EPOLLIN,':',event & select.EPOLLIN)
				print('cli data input:%s' % fileno)
				try:
					info = conns[fileno].recv(5)
					request[fileno] += info	
					print('%s:%s,data:%s' %(fileno,info,request[fileno]))
					if not info:
						raise ConnectionResetError('没有数据')
					epoll_loop.modify(fileno,select.EPOLLOUT)
				except ConnectionResetError as e:
					'''
					客户端关闭
					'''
					print('cli %s close/%s' % (fileno,e))
					epoll_loop.unregister(fileno)
					conns[fileno].close()
					request.pop(fileno)
					if fileno in response:
						response.pop(fileno) 
			elif event & select.EPOLLOUT:				
				try:
					data = request[fileno]
					ret = conns[fileno].sendall(data)
					print('cli data output:%s,data:%s,ret:%s' % (fileno,data,ret))
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
				
			
			
		