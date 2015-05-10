#
# Peer.py
# ?
#
# Jonatan H Sundqvist
# May 10 2015
#

# TODO | - Synchronise calls to send/receive (thread safety) (?)
#        - 

# SPEC | -
#        -



import socket
import threading
import pickle



class Peer(object):

	'''
	Docstring goes here

	'''


	def __init__(self, IP, port, onreceive):

		'''
		Docstring goes here

		'''

		# Configurations
		self.running = True

		#
		self.onreceive = onreceive  #

		#
		self.address   = (IP, port)     # Port and IP of the server (not the Peer itself)
		self.socket    = self.connect() # Server socket

		#
		self.thread = threading.Thread(target=lambda: self.protocol(), daemon=True).start() #



	def connect(self):

		'''
		Repeatedly attempt to connect to a server, until it succeeds

		'''

		# TODO: Delay
		# Server socket
		server = socket.socket() # TODO: Arguments

		while True:
			try:
				print('Attempting to connect to {0:}'.format(self.address[0]))
				server.connect(self.address)
				print('Succeeded to connect.')
				return server
			except:
				# TODO: Wait (cf. delay)
				print('Failed to connect to {0:}'.format(self.address[0]))
				# print('Retrying after {0:} seconds'.format(delay))


	def protocol(self):
		
		'''
		Doctring goes here

		'''

		# TODO: Expect Packages 

		while True:
			print('Client running protocol')
			try:
				# TODO: Handle blocks
				size = int(self.socket.recv(4).decode('UTF-8')) # Read size prefix (padded to four digits)
				data = self.socket.recv(size)                   # Read data

				# data = pickle.loads(received) # TODO: Allow custom action (other than pickle; cf. Package.action)
				print('Peer received {0:} bytes from server.'.format(size)) # TODO: Print representation of incoming data (?)
				self.onreceive(data)
			except Exception as e:
				print(e)
				print('Lost connection with server')
				return False # TODO: Meaningful return values (?)


		print('Client somehow escaped protocol loop')


	def send(self, data):

		'''
		Docstring goes here

		'''

		# TODO: Use Package
		# TODO: Custom actions (cf. Package)
		# TODO: Callback for sending successfully

		# TODO: Move this routine (send data with padded size information) to separate function
		# self.socket.send(bytes('{size:04d}'.format(size=len(data)), encoding='UTF-8'))
		# self.socket.send(pickle.dumps(data)) # TODO: Pickle by default (?)
		return self.socket.send(bytes('{0:04d}'.format(len(data)), 'UTF-8') + data)




def main():
	
	'''
	Docstring goes here

	'''

	peer = Peer('localhost', 255, onreceive=lambda data: print('Message: {msg}'.format(msg=pickle.loads(data))))

	while True:
		post = input('Say something: ')
		peer.send(pickle.dumps(post))



if __name__ == '__main__':
	main()