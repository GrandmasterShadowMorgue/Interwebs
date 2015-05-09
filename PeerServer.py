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



class Peer(object):

	'''
	Docstring goes here

	'''

	def __init__(self, server):
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

	def __init__(self, port, ip, protocol, onsend, onreceive):

		'''
		Docstring goes here

		'''

		# Configurations
		self.running = True #
		self.maximum = 5    # Maximum number of simultaneous peers

		# Protocol
		# TODO: Decide exactly how to deal with these (default protocol?)
		self.protocol  = protocol  #
		self.onsend    = onsend    #
		self.onreceive = onreceive #

		# 
		self.address      = (ip, port)      # TODO: Use namedtuple (?)
		self.listenSocket = socket.socket() # TODO: Arguments
		self.connections  = []              # Connected peers (TODO: other type, eg. dict mapping IDss to connections?)

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
		# TODO: Protocol for adding new peer (initial handshake, eg. assign ID, passwords, username, 'explain' protocol, etc.)
		peer = self.listenSocket.accept() #
		self.connections.append(peer)     #
		print('Accepted peer #{0}: {1}'.format(len(self.connections), peer)) # TODO: Printable clients (eg. username, ID)

		return peer


	def disconnect(self, peer):

		'''
		Docstring goes here

		'''

		pass


	def send(self, data):
		
		'''
		Docstring goes here

		'''

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