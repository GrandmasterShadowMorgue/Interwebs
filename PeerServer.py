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
#        - Match ID to socket object (?)

# SPEC | -
#        -



# Core
import socket
import threading
import pickle
import queue
import time

import uuid #
import enum #

import Protocols
from Protocols import Event

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
		self.debug   = True
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
			Event.Data         : lambda packet: self.broadcast(packet), # - A Peer is sending data
			Event.Disconnect   : lambda packet: None, # - A Peer has disconnected
			Event.Connect      : lambda packet: None, # - A Peer is attempting to connect
			Event.Verify       : lambda packet: None, # - A Peer verifies that it has received a Packet
			Event.Introduce    : lambda packet: None, # - A Peer introduces itself (username, id, etc.)
			Event.Authenticate : lambda packet: None  # - Server is authenticating a peer (currently: sends an ID)
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
		self.log('Waiting for incoming peers...')

		sock = self.listenSocket.accept() #
		peer = Protocols.Peer(ID=uuid.uuid1(), socket=sock, thread=None)
		peer.thread = self.handshake(peer)

		# TODO: How to deal with Server packets
		# TODO: Flesh out authentication process
		self.send(peer, Protocols.Packet(event=Event.Authenticate, action=None, sender='Server', data=pickle.dumps(peer.ID), recipients=None))

		self.connections[peer.ID] = peer #
		self.log('Accepted peer #{0}: {1}\n\n'.format(len(self.connections), peer.ID)) # TODO: Printable clients (eg. username, ID)

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

		# TODO: Expect packets
		# TODO: Expect Peers

		# TODO: Unsafe to use multiple threads without syncing (?)

		while True:
			self.log('Running protocol with {0}'.format(peer.ID))
			try:
				# TODO: Handle blocks
				packet = self.receive(peer)
				# self.log('\n\nReceived data from peer {0}'.format(peer.ID))
				self.log('\n\nServer received {0:} bytes from {1:} ({2!r}).'.format(len(packet.data), peer.ID, packet.event)) # TODO: Print representation of incoming data (?)
				self.callbacks[packet.event](packet) # TODO: Not sure if this should be here...
			# except ConnectionResetError
			except Exception as e:
				self.log(type(e))
				self.log(e)
				self.log('Lost connection with {0:}.'.format(peer.ID))
				# TODO: Remove peer from list
				# TODO: Disconnection protocol (eg. tell other peers) (?)
				return False # TODO: Meaningful return values (?)

			# data = pickle.loads(received) # TODO: Allow custom action (other than pickle; cf. packet.action)
			# self.log('Server received {0:} bytes from {1:}.'.format(len(packet.data), peer)) # TODO: Print representation of incoming data (?)

			# self.broadcast(packet)



	def disconnect(self, peer):

		'''
		Docstring goes here

		'''

		pass


	def broadcast(self, packet):

		'''
		Docstring goes here

		'''

		assert all(ID == peer.ID for ID, peer in self.connections.items()), 'Strange...'
		recipients = lambda: (recipient for recipient in self.connections.values() if recipient.ID != packet.sender)
		print('Broadcasting to {0} peers.'.format(sum(1 for r in recipients())))

		for recipient in recipients():
				# if (recipient.ID != packet.sender) and (packet.recipients is None or recipient.ID in packet.recipients):
				self.send(recipient, packet)


	def send(self, peer, packet):
		
		'''
		Send data (raw bytes) to a specific peer.

		'''

		# NOTE: Peer is currently assumed to be a socket (should eventually be a PeerServer.Peer wrapper object)

		# TODO: Send to all peers by default (?)
		# TODO: Handle data sizes greater than 9999
		# TODO: Configure data size cap (?)

		data = pickle.dumps(packet)

		if len(data) > 9999:
			self.log('Unable to send more than 9999 bytes of data at a time ({size} is too much)'.format(size=len(data)))
		else:
			# TODO: Safe to send in two separate calls (?)
			# TODO: Inefficient to concatenate bytes (use bytearray?)
			self.log('Server is sending {size} bytes of data to {peer}'.format(size=len(data), peer=peer.ID))
			# peer.send(bytes('{size:04d}'.format(size=len(data)), encoding='UTF-8'))
			# peer.send(data)
			# return peer.socket[0].send(bytes('{0:04d}'.format(len(data)), 'UTF-8') + data)
			return Protocols.sendRaw(peer.socket[0], data, padding=4)


	def receive(self, peer):
		
		'''
		Docstring goes here

		'''

		return Protocols.receive(peer.socket[0])


	def log(self, msg, level=None):
		if self.debug: print(msg)



def main():
	
	'''
	Docstring goes here

	'''

	server = PeerServer('localhost', 255) # , onsend=None, onreceive=None
	server.start()


if __name__ == '__main__':
	main()