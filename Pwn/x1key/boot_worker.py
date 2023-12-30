import struct
import os
import sys
import uuid
import subprocess
import socket
import time

boot_cmd="./start.sh "

def auth():
	return 1

if __name__ == '__main__':
	if (auth()!=1):
		print("Error: Authenticate Failure")
		exit(-1)

	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect(("127.0.0.1", 9999))

	print("Please waiting for resourse allocation......")
	sys.stdout.flush()

	(port, ) = struct.unpack("!h", sock.recv(2))

	password = "4796712a-31e3-481a-8f11-2c5fc72bee7b"

	print("Qemu is starting now. Please waiting for a second\n")
	print("\tssh ctf@kagehutatsu.com -p " + str(port))
	print("\tpassword: " + password)
	print("\nDon\'t close this connect and start a new terminal")
	print("You have 2min to upload and execute ur poc")
	sys.stdout.flush()

	process = subprocess.run(["./start.sh", str(port)], stdout = subprocess.DEVNULL)

	print("Timeout. Bye ~")
	sys.stdout.flush()

	sock.close()
