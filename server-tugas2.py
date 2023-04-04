from socket import *
import socket
import threading
import logging
import time
import sys
from datetime import datetime

class ProcessTheClient(threading.Thread):
	def __init__(self,connection,address):
		self.connection = connection
		self.address = address
		threading.Thread.__init__(self)

	def run(self):
		while True:
			data = self.connection.recv(32)
			data_string = data.decode()
			if data:
				data_front = data_string[:4]
				data_back = data_string[-4:]
				print(data_front, data_back)
				if(data_front == 'TIME' and data_back == '1310'):
					currentDateAndTime = datetime.now()
					currentTime = currentDateAndTime.strftime("%H:%M:%S")
					reply = "JAM " + currentTime + " 1310"
					self.connection.sendall(reply.encode())
				else:
					reply = "Request rejected"
					self.connection.sendall(reply.encode())
			else:
				break
		self.connection.close()

class Server(threading.Thread):
	def __init__(self):
		self.the_clients = []
		self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		threading.Thread.__init__(self)

	def run(self):
		self.my_socket.bind(('0.0.0.0',45000))
		self.my_socket.listen(1)
		while True:
			self.connection, self.client_address = self.my_socket.accept()
			logging.warning(f"connection from {self.client_address}")
			
			clt = ProcessTheClient(self.connection, self.client_address)
			clt.start()
			self.the_clients.append(clt)
	

def main():
	svr = Server()
	svr.start()

if __name__=="__main__":
	main()