#-*- coding:utf-8 -*-
from select import select 
import queue
import socket
addr= ('127.0.0.1',9999)
ser = socket.socket()
ser.bind(addr)
ser.setblocking(False)
ser.listen(2)
input_list = []
output_list = []
meg = {}
input_list.append(ser)	
print('runing')
while True:
	print('waiting event change...')
	in_list,out_list,err = select(input_list,output_list,input_list)
	if out_list:
		print('out_list:',out_list)
	if err:
		print('err:',err)
	for input in in_list:
		if input == ser:
			conn,addr = input.accept()
			print('%s:comme in' % conn)
			if conn not in input_list:
				print('add cli into listen')
				input_list.append(conn)
				meg[conn] = queue.Queue()
		else:
			try:				
				data = input.recv(1024)
				if data:
					data = data.decode()
					print('cli input:%s' % data)
					meg[input].put(data)
					if input not in output_list:
						print('add cli out into output_list')
						output_list.append(input)
						
			except ConnectionResetError:
				input_list.remove(input)
				output_list.remove(input)
				del meg[input]
				print('%s:close' % input)
	for output in output_list:
		try:
			print('write info to cli')
			if not meg[output].empty():
				send_data = meg[output].get()
				print('send_data:%s' % send_data)
				ret = output.sendall(b'a')
				print('send_ret:%s' % ret)
				output_list.remove(output)
			else:
				output_list.remove(output)
		except ConnectionResetError:
			input_list.remove(output)
			output_list.remove(output)
			del meg[output]
			print('%s:close' % output)