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
#        - Proper logging
#        - Move common utilities to separate module

# SPEC | -
#        -



# Core
import socket
import threading
import pickle
import queue
import time

import uuid #
import Enum

import Protocols

# Testing
# import 



class PeerServer(object):

	'''
	Docstring goes here

	'''

	# TODO: Separate client and server (?)
	# TODO: Encapsulate each connection (Peer) in an object (?)
	# TODO: Rename to Peer (?)

	# TODO: Initial handshake

	def __init__(self, IP, port):

		'''
		Docstring goes here

		'''

		# Configurations
		self.running = True #
		self.maximum = 5    # Maximum number of simultaneous peers

		# Protocol
		# TODO: Decide exactly how to deal with these (default protocol?)

		# The callbacks should allow users of this library to customise the protocol for
		# sending and receiving data (just for peers or for the server too?)
		#
		# Should peers be allowed to choose which peers to communicate with each time?

		# self.protocol  = protocol #
		# self.onsend    = onsend    # 
		# self.onreceive = onreceive
		self.callbacks = {
			Event.Data         : lambda package: self.broadcast(package), # - A Peer is sending data
			Event.Disconnect   : lambda package: None, # - A Peer has disconnected
			Event.Connect      : lambda package: None, # - A Peer is attempting to connect
			Event.Verify       : lambda package: None, # - A Peer verifies that it has received a package
			Event.Introduce    : lambda package: None, # - A Peer introduces itself (username, id, etc.)
			Event.Authenticate : lambda package: None  # - Server is authenticating a peer (currently: sends an ID)
		}

		# 
		self.address      = (IP, port)      # TODO: Use namedtuple (?)
		self.listenSocket = socket.socket() # TODO: Arguments
		self.connections  = {}              # Connected peers (TODO: other type, eg. dict mapping IDs to connections?)

		self.listenSocket.bind(self.address)   #
		self.listenSocket.listen(self.maximum) #


	def start(self):
		
		'''
		Docstring goes here

		'''

		# TODO: Allow user to enter main loop themselves (eg. add a start or server_forever method) (✓)
		# Main loop (keep accepting incoming connections)
		while self.running and self.maximum > len(self.connections):
			self.connect() #


	def connect(self):

		'''
		Docstring goes here

		'''

		# TODO: Rename (eg. listen, acceptPeer) (?)

		# 
		# TODO: Timeout
		# TODO: Protocol for adding new peers (initial handshake, eg. assign ID, passwords, username, 'explain' protocol, etc.)
		self.log('Listening for incoming peers...')

		sock = self.listenSocket.accept() #
		peer = Protocols.Peer(id=uuid.uuid1(), socket=sock, thread=self.handshake(sock))

		self.connections[peer.id] = peer #
		self.log('Accepted peer #{0}: {1}'.format(len(self.connections), peer)) # TODO: Printable clients (eg. username, ID)

		return peer


	def handshake(self, peer):
		
		'''
		Docstring goes here

		'''

		# TODO: Other handshake actions
		# TODO: Customisation
		# TODO: Save thread reference (cf. Peer.thread)
		thread = threading.Thread(target=lambda: self.protocol(peer), daemon=True)
		thread.start() #
		return thread  #


	def protocol(self, peer):
		
		'''
		Defines the protocol for the server and a single peer

		'''

		# TODO: Expect Packages
		# TODO: Expect Peers

		# TODO: Unsafe to use multiple threads without syncing (?)

		while True:
			self.log('Running protocol with {0}'.format(peer))
			try:
				# TODO: Handle blocks
				package = self.receive(peer)
			except Exception as e:
				self.log(type(e))
				self.log(e)
				self.log('Lost connection with {0:}.'.format(peer))
				# TODO: Remove peer from list
				# TODO: Disconnection protocol (eg. tell other peers) (?)
				return False # TODO: Meaningful return values (?)

			# data = pickle.loads(received) # TODO: Allow custom action (other than pickle; cf. Package.action)
			self.log('Server received {0:} bytes from {1:}.'.format(size, peer)) # TODO: Print representation of incoming data (?)

			self.broadcast(package)



	def disconnect(self, peer):

		'''
		Docstring goes here

		'''

		pass


	def broadcast(self, package):

		'''
		Docstring goes here

		'''

		for recipient in self.connections.values():
				if (recipient.id != package.sender) and (package.recipients is None or recipient.id in package.recipients):
					self.send(recipient, package)


	def send(self, peer, package):
		
		'''
		Send data (raw bytes) to a specific peer.

		'''

		# NOTE: Peer is currently assumed to be a socket (should eventually be a PeerServer.Peer wrapper object)

		# TODO: Send to all peers by default (?)
		# TODO: Handle data sizes greater than 9999
		# TODO: Configure data size cap (?)

		if len(data) > 9999:
			self.log('Unable to send more than 9999 bytes of data at a time ({size} is too much)'.format(size=len(data)))
		else:
			# TODO: Safe to send in two separate calls (?)
			# TODO: Inefficient to concatenate bytes (use bytearray?)
			self.log('Server is sending {size} bytes of data to {peer}'.format(size=len(data), peer=peer))
			# peer.send(bytes('{size:04d}'.format(size=len(data)), encoding='UTF-8'))
			# peer.send(data)
			return peer.socket[0].send(bytes('{0:04d}'.format(len(data)), 'UTF-8') + data)


	def receive(self, peer):
		
		'''
		Docstring goes here

		'''

		size = int(peer[0].recv(4).decode('UTF-8')) # Read size prefix (padded to four digits)
		data =  peer[0].recv(size)                  # Read data
		package = pickle.loads(data)

		return self.callbacks[package.event](package) #


	def log(self, msg, level=None):
		if self.debug: print(msg)



def main():
	
	'''
	Docstring goes here

	'''

	server = PeerServer('localhost', 255, onsend=None, onreceive=None)
	server.start()


if __name__ == '__main__':
	main()