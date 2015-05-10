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

import Protocols



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
		# self.onreceive = onreceive  #
		self.callbacks = {
			Event.Data         : lambda package: onreceive(package), # - A Peer is sending data
			Event.Disconnect   : lambda package: None,               # - A Peer has disconnected
			Event.Connect      : lambda package: None,               # - A Peer is attempting to connect
			Event.Verify       : lambda package: None,               # - A Peer verifies that it has received a package
			Event.Introduce    : lambda package: None,               # - A Peer introduces itself (username, id, etc.)
			Event.Authenticate : lambda package: None                # - Server is authenticating a peer (currently: sends an ID)
		}

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
				self.log('Attempting to connect to {0:}'.format(self.address[0]))
				server.connect(self.address)
				self.log('Succeeded to connect.')
				return server
			except:
				# TODO: Wait (cf. delay)
				self.log('Failed to connect to {0:}'.format(self.address[0]))
				# print('Retrying after {0:} seconds'.format(delay))


	def protocol(self):
		
		'''
		Doctring goes here

		'''

		# TODO: Expect Packages 

		while True:
			self.log('Client running protocol')
			try:
				# TODO: Handle blocks
				size = int(self.socket.recv(4).decode('UTF-8')) # Read size prefix (padded to four digits)
				data = self.socket.recv(size)                   # Read data
				package = pickle.loads(data)                    #

				# data = pickle.loads(received) # TODO: Allow custom action (other than pickle; cf. Package.action)
				self.log('Peer received {0:} bytes from server.'.format(size)) # TODO: Print representation of incoming data (?)
				self.callbacks[package.event](package) #
				# self.onreceive(data)
			except Exception as e:
				# TODO: Split exception handling when we're done debugging
				self.log(e)
				self.log('Lost connection with server')
				return False # TODO: Meaningful return values (?)

		self.log('Client somehow escaped protocol loop')


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


	def log(self, msg, level=None):
		if self.debug: print(msg)



def main():
	
	'''
	Docstring goes here

	'''

	peer = Peer('localhost', 255, onreceive=lambda package: print('Message: {msg}'.format(msg=pickle.loads(package.data))))

	while True:
		post = input('Say something: ')
		peer.send(pickle.dumps(post))



if __name__ == '__main__':
	main()