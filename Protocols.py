#
# Protocols.py
# ?
#
# Jonatan H Sundqvist
# May 11 2015
#

# TODO | - 
#        - 

# SPEC | -
#        -



import time
import enum



# Data         - A Peer is sending data
# Disconnect   - A Peer has disconnected
# Connect      - A Peer is attempting to connect
# Verify       - A Peer verifies that it has received a package
# Introduce    - A Peer introduces itself (username, id, etc.)
# Authenticate - Server is authenticating a peer (currently: sends an ID)
Event = enum.Enum('Event', 'Data Disconnect Connect Verify Introduce Authenticate')



class Packet(object):
	# TODO: Rename message (would also handle verification, disconnects, etc.) (?)
	# TODO: Add event tags (data, disconnect, etc.)
	# TODO: Security (eg. avoid arbitrary callables as actions; maybe Enum instead mapped to allowed actions)
	def __init__(self, event, action, sender, data, recipients=None):
		self.timestamp  = time.time() # TODO: UTC seconds
		self.event      = event       # Should be an Event enum (?)
		self.sender     = sender      # TODO: How to encode sender (?)
		self.data       = data        #
		self.recipients = recipients  # A set of peer IDs (allows Packets to be directed to specific peers)
		self.action     = None        #



class Peer(object):

	'''
	This class represents a peer from the point of view of the server
	(which mediates the exchange of data between peers).

	'''

	# TODO: Rename to desambiguate (or replace with namedtuple) (?)

	def __init__(self, ID, socket, thread):
		self.ID     = ID     #
		self.socket = socket #
		self.thread = thread #
		# self.name   = None   #



def send(self, socket, data, padding):

	'''
	Docstring goes here

	'''

	# TODO: Encode action parameter
	# TODO: Use Packet

	pass



def sendRaw(socket, data, padding):

	'''
	Docstring goes here

	'''

	return socket.send(bytes(('{0:0%dd}' % padding).format(len(data)), 'UTF-8') + data)



def receive(socket, timeout=0):
		
	'''
	Docstring goes here

	'''

	size = int(socket.recv(4).decode('UTF-8')) # Read size prefix (padded to four digits)
	data = socket.recv(size)                   # Read data
	packet = pickle.loads(data)                        #

	return packet



def main():
	
	'''
	Docstring goes here

	'''

	pass



if __name__ == '__main__':
	main()