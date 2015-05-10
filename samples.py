#
# samples.py
# ?
#
# Jonatan H Sundqvist
# May 10 2015
#

# TODO | - 
#        - 

# SPEC | -
#        -



import PeerServer
import Peer

import tkinter as tk
import tkinter.ttk as ttk

import pickle



class ChatClient(object):

	'''
	Docstring goes here

	'''


	def __init__(self):
		
		'''
		Docstring goes here

		'''

		self.size = 480, 720

		# Create the window
		self.window = tk.Tk()
		# self.window.geometry('{width}x{height}'.format(width=self.size[0], height=self.size[1]))
		self.window.title('Chat')

		# Create the interface
		self.write = ttk.Entry()
		self.write.grid(column=0, row=1)
		# self.write.pack()
		self.write.bind('<Return>', lambda e: self.postEntry(self.write.get()))

		self.entryFrame = ttk.Frame() # width=self.size[0], height=self.size[1]-30
		self.entryFrame.grid(column=0, row=0)
		# self.entryFrame.pack()

		self.entries = []

		#
		# TODO: This is a HORRIBLE solution
		# if input('Would you like to create a server? ').lower() in ('yes', 'true', 'y', 'yeah'):
			# server = PeerServer.PeerServer('localhost', 255, onsend=None, onreceive=None)

		self.peer = Peer.Peer('localhost', 255, onreceive=lambda data: self.addEntry(pickle.loads(data)))

		#
		self.window.mainloop()


	def postEntry(self, message):

		'''
		Docstring goes here

		'''

		self.addEntry(message)
		self.peer.send(pickle.dumps(message))


	def addEntry(self, message):

		'''
		Docstring goes here

		'''

		print('Received message:', message)
		entry = ttk.Label(master=self.entryFrame, text=message)
		entry.grid(column=0, row=len(self.entries))
		# entry.pack()
		self.entries.append(entry)
		# entry.pack()




def main():

	'''
	Docstring goes here

	'''

	#
	app = ChatClient()


if __name__ == '__main__':
	main()