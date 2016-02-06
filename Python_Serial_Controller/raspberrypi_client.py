import socket

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.connect(('', 1336))
socket.send('raspberrypi\n')

while True:
	print socket.recv(1024)
