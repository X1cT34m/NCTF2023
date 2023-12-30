import struct
import threading
import subprocess
import time
import socket

port_list={11231, 21032, 36123, 21314, 24875, 15932, 28032, 19283, 28123}

def acquire_port():
	global port_list
	
	while (True):
		lock.acquire()
		
		if (len(port_list) != 0):
			port = port_list.pop()
		else:
			port = -1
					
		lock.release()
		
		if (port != -1):
			return port
		else:
			time.sleep(2)

def release_port(port):
	lock.acquire()
	
	global port_list
	port_list.add(port)
	
	lock.release()
	
def thread_alloc(connect):
	connect.settimeout(180)
	try:
		
		port = acquire_port()
		print("acquire "+str(port))
		connect.send(struct.pack('!h',port))
		
		connect.recv(1)
		
	except ConnectionResetError:
		print("connect close")
	except socket.timeout:
		print("connect timeout")
	
	release_port(port)
	print("release "+str(port))
	connect.close()
			

if __name__ == '__main__':
	lock = threading.Lock()
	
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.bind(("127.0.0.1", 9999))
	sock.listen(100)
	
	while (True):
		connect, address = sock.accept()
		
		subThread = threading.Thread(target = thread_alloc, args = (connect,))
		subThread.start()
		
			
		
		


