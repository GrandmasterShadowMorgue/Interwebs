#
# PeerServer.py
# ?
#
# Jonatan H Sundqvist
# May 09 2015
#

# TODO | - Figure out API
#        - Multiple Peers
#        - Samples and tests
#        - Safety (https, passwords)
#        - Lists of known connections, profiles
#        - Different protocols, threading (?)
#        - Events (eg. peer disconnected, incoming data) (as tagged unions?)
#        - Command line interface (?)

# SPEC | -
#        -



# Core
import socket
import threading
import pickle
import queue
import time

# Testing
# import 



class Packet(object):
	# TODO: Add event tags (data, disconnect, etc.)
	def __init__(self, sender, data):
		self.timestamp = 0 # TODO: UTC seconds
		self.sender    = sender # TODO: How to encode sender (?)
		self.data      = data
		self.action    = None



class Peer(object):

	'''
	This class represents a peer from the point of view of the server
	(which mediates the exchange of data between peers).

	'''

	def __init__(self):
		self.id     = None #
		self.name   = None #
		self.socket = None #
		self.thread = None #



class PeerServer(object):

	'''
	Docstring goes here

	'''

	# TODO: Separate client and server (?)
	# TODO: Encapsulate each connection (Peer) in an object (?)
	# TODO: Rename to Peer (?)

	# TODO: Initial handshake

	def __init__(self, port, ip, onsend, onreceive):

		'''
		Docstring goes here

		'''

		# Configurations
		self.running = True #
		self.maximum = 5    # Maximum number of simultaneous peers

		# Protocol
		# TODO: Decide exactly how to deal with these (default protocol?)
		# The callbacks should allow users of this library to customise the protocol for
		# Should peers be allowed to choose which peers to communicate with each time?
		# sending and receiving data (just for peers or for the server too?)
		# self.protocol  = protocol #
		self.onsend    = onsend    # 
		self.onreceive = onreceive # What should happen when the server receives data from a peer ()

		# 
		self.address      = (ip, port)      # TODO: Use namedtuple (?)
		self.listenSocket = socket.socket() # TODO: Arguments
		self.connections  = []              # Connected peers (TODO: other type, eg. dict mapping IDs to connections?)

		self.listenSocket.bind(self.address) #

		# Main loop (keep accepting incoming connections)
		while self.running and self.maximum < len(self.connections):
			#
			self.connect()


	def connect(self):

		'''
		Docstring goes here

		'''

		# TODO: Rename (eg. listen, acceptPeer) (?)

		# 
		# TODO: Timeout
		# TODO: Protocol for adding new peers (initial handshake, eg. assign ID, passwords, username, 'explain' protocol, etc.)
		peer = self.listenSocket.accept() #
		self.connections.append(peer)     #
		print('Accepted peer #{0}: {1}'.format(len(self.connections), peer)) # TODO: Printable clients (eg. username, ID)

		return peer


	def handshake(self, peer):
		
		'''
		Docstring goes here

		'''

		pass


	def protocol(self, peer):
		
		'''
		Defines the protocol for the server and a single peer

		'''

		# TODO: Expect Packages
		# TODO: Expect Peers

		while True:
			try:
				size = int(peer.recv(4).decode('UTF-8')) # Read size prefix (padded to four digits)
				received = peer.recv(size)               # Read data
			except:
				print('Lost connection with {0:}.'.format(peer))
				# TODO: Remove peer from list
				# TODO: Disconnection protocol (eg. tell other peers) (?)
				return False # TODO: Meaningful return values (?)

			data = pickle.loads(received) # TODO: Allow custom action (other than pickle; cf. Package.action)
			print('Server received {0:} bytes from {1:}.'.format(size, peer)) # TODO: Print representation of incoming data (?)

			for recipient in filter(lambda recipient: recipient != peer, self.connections):
				self.send(recipient, data)



	def disconnect(self, peer):

		'''
		Docstring goes here

		'''

		pass


	def send(self, peer, data):
		
		'''
		Docstring goes here

		'''

		# TODO: Send to all peers by default (?)

		pass


	def receive(self, peer):
		
		'''
		Docstring goes here

		'''

		pass



def main():
	
	'''
	Docstring goes here

	'''

	pass



if __name__ == '__main__':
	main()