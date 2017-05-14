import socket
ser = socket.socket()
ser.connect(('127.0.0.1',9999))
ser.send(b'hello world')