#
# Peer.py
# ?
#
# Jonatan H Sundqvist
# May 10 2015
#

# TODO | - Synchronise calls to send/receive (thread safety) (?)
#        - Event based API (?)
#        - Handle exceptions and errors

# SPEC | -
#        -



import socket
import threading
import pickle

from Interwebs import Protocols
from Interwebs.Protocols import Event, Packet



class Peer(object):

	'''
	Docstring goes here

	'''


	def __init__(self, IP, port, onreceive, onconnect, onauthenticated=None, ondisconnect=None):

		'''
		Docstring goes here

		'''

		# Configurations
		self.running = True
		self.debug   = True

		#
		# self.onreceive = onreceive  #
		# TODO: Use callbacks.update to override default callbacks (?)
		self.onauthenticated = onauthenticated or (lambda ID: print('Peer {0} has been authenticated'.format(ID)))
		self.ondisconnect    = ondisconnect    or (lambda ID: print('Peer {0} has disconnected'.format(ID)))
		self.callbacks = {
			Event.Data         : lambda packet: onreceive(packet.sender, pickle.loads(packet.data)),      # - A Peer is sending data (give clients access to the entire packet?)
			Event.Disconnect   : lambda packet: self.ondisconnect(packet.sender),                         # - A Peer has disconnected
			Event.Connect      : lambda packet: onconnect(packet.sender, pickle.loads(packet.data)), # - A Peer is attempting to connect (eg. ANOTHER peer)
			Event.Verify       : lambda packet: None,                                                     # - A Peer verifies that it has received a packet
			Event.Introduce    : lambda packet: None,                                                     # - A Peer introduces itself (username, id, etc.)
			Event.Authenticate : lambda packet: self.authenticate(packet) # - Server is authenticating this peer (currently: sends an ID)
		}

		#
		self.address   = (IP, port)     # Port and IP of the server (not the Peer itself)
		self.socket    = self.connect() # Server socket

		#
		self.ID     = None
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

		# TODO: Expect packets 

		while True:
			self.log('Client running protocol')
			try:
				# TODO: Handle blocks
				packet = Protocols.receive(self.socket)

				# data = pickle.loads(received) # TODO: Allow custom action (other than pickle; cf. packet.action)
				# self.log('Peer received {0} bytes from server ({1}).'.format(len(packet.data), packet.event)) # TODO: Print representation of incoming data (?)
				self.callbacks[packet.event](packet) #
				# self.onreceive(data)
			# except Exception as e:
			except ValueError as e:
				# TODO: Split exception handling when we're done debugging
				self.log(type(e))
				self.log(e)
				self.log('Lost connection with server')
				return False # TODO: Meaningful return values (?)

		self.log('Client somehow escaped protocol loop')


	def authenticate(self, packet):

		'''
		Docstring goes here

		'''

		self.log('Authenticated by server')
		self.ID = pickle.loads(packet.data) # The ID chosen by the server for this Peer is stored in the data field
		self.onauthenticated(self.ID)


	def send(self, data, event=Event.Data, recipients=None):

		'''
		Docstring goes here

		'''

		# TODO: Use packet
		# TODO: Custom actions (cf. packet)
		# TODO: Callback for sending successfully

		# TODO: Use this method for other events too (other than data?)

		# TODO: Move this routine (send data with padded size information) to separate function
		# self.socket.send(bytes('{size:04d}'.format(size=len(data)), encoding='UTF-8'))
		# self.socket.send(pickle.dumps(data)) # TODO: Pickle by default (?)

		# print('Peer is sending data (ID={0}, event={1})'.format(self.ID, event))
		packet = Packet(event=event, action=None, sender=self.ID, data=data, recipients=recipients)

		return Protocols.sendRaw(self.socket, pickle.dumps(packet), padding=4)


	def log(self, msg, level=None):
		if self.debug: print(msg)



def main():
	
	'''
	Docstring goes here

	'''

	def onreceive(data):
		print('Inside onreceive callback')
		print('Message: {msg}'.format(msg=data))

	peer = Peer('localhost', 255, onreceive=onreceive, onconnect=lambda *args: None)

	while True:
		post = input('Say something: ')
		peer.send(pickle.dumps(post))



if __name__ == '__main__':
	main()