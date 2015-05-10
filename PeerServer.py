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
	# TODO: Rename message (would also handle verification, disconnects, etc.) (?)
	# TODO: Add event tags (data, disconnect, etc.)
	# TODO: Security (eg. avoid arbitrary callables as actions; maybe Enum instead mapped to allowed actions)
	def __init__(self, sender, data):
		self.timestamp = 0      # TODO: UTC seconds
		self.event     = None   # Should be an Event enum (?)
		self.sender    = sender # TODO: How to encode sender (?)
		self.data      = data   #
		self.action    = None   #



class Peer(object):

	'''
	This class represents a peer from the point of view of the server
	(which mediates the exchange of data between peers).

	'''

	# TODO: Rename to desambiguate (or replace with namedtuple) (?)

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

	def __init__(self, IP, port, onsend, onreceive):

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
		#
		# 

		# self.protocol  = protocol #
		self.onsend    = onsend    # 
		self.onreceive = onreceive # What should happen when the server receives data from a peer ()

		# 
		self.address      = (IP, port)      # TODO: Use namedtuple (?)
		self.listenSocket = socket.socket() # TODO: Arguments
		self.connections  = []              # Connected peers (TODO: other type, eg. dict mapping IDs to connections?)

		self.listenSocket.bind(self.address)   #
		self.listenSocket.listen(self.maximum) #

		# TODO: Allow user to enter main loop themselves (eg. add a start or server_forever method)
		# Main loop (keep accepting incoming connections)
		while self.running and self.maximum > len(self.connections):
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
		print('Listening for incoming peers...')
		peer = self.listenSocket.accept() #
		self.connections.append(peer)     #
		print('Accepted peer #{0}: {1}'.format(len(self.connections), peer)) # TODO: Printable clients (eg. username, ID)

		self.handshake(peer)

		return peer


	def handshake(self, peer):
		
		'''
		Docstring goes here

		'''

		# TODO: Other handshake actions
		# TODO: Customisation
		# TODO: Save thread reference (cf. Peer.thread)
		return threading.Thread(target=lambda: self.protocol(peer), daemon=True).start() #


	def protocol(self, peer):
		
		'''
		Defines the protocol for the server and a single peer

		'''

		# TODO: Expect Packages
		# TODO: Expect Peers

		# TODO: Unsafe to use multiple threads without syncing (?)

		while True:
			print('Running protocol with {0}'.format(peer))
			try:
				# TODO: Handle blocks
				size = int(peer[0].recv(4).decode('UTF-8')) # Read size prefix (padded to four digits)
				data = peer[0].recv(size)                   # Read data
			except Exception as e:
				print(e)
				print('Lost connection with {0:}.'.format(peer))
				# TODO: Remove peer from list
				# TODO: Disconnection protocol (eg. tell other peers) (?)
				return False # TODO: Meaningful return values (?)

			# data = pickle.loads(received) # TODO: Allow custom action (other than pickle; cf. Package.action)
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
		Send data (raw bytes) to a specific peer.

		'''

		# NOTE: Peer is currently assumed to be a socket (should eventually be a PeerServer.Peer wrapper object)

		# TODO: Send to all peers by default (?)
		# TODO: Handle data sizes greater than 9999
		# TODO: Configure data size cap (?)

		if len(data) > 9999:
			print('Unable to send more than 9999 bytes of data at a time ({size} is too much)'.format(size=len(data)))
		else:
			# TODO: Safe to send in two separate calls (?)
			# TODO: Inefficient to concatenate bytes (use bytearray?)
			print('Server is sending {size} bytes of data to {peer}'.format(size=len(data), peer=peer))
			# peer.send(bytes('{size:04d}'.format(size=len(data)), encoding='UTF-8'))
			# peer.send(data)
			return peer[0].send(bytes('{0:04d}'.format(len(data)), 'UTF-8') + data)



	def receive(self, peer):
		
		'''
		Docstring goes here

		'''

		pass



def main():
	
	'''
	Docstring goes here

	'''

	server = PeerServer('localhost', 255, onsend=None, onreceive=None)


if __name__ == '__main__':
	main()