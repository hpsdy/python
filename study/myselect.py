import socket
ser = socket.socket()
#ser.setblocking(False)
ser.bind(('127.0.0.1',9999))
ser.listen(5)
while True:
	try:
	    cli,addr = ser.accept()
	    print('blocking until cli',cli,':',addr)
	    while True:
	    	print('begin',"\n")
	    	data = cli.recv(1024)
	    	print('get info',"\n")
	    	if data:
	    		print(data.decode())
	    	else:
	    		cli.close()
	    		break
	except BlockingIOError as e:
		pass
		