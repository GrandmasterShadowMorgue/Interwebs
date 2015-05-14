#
# chat.py
# ?
#
# Jonatan H Sundqvist
# May 13 2015
#

# TODO | - 
#        - 

# SPEC | -
#        -



from Interwebs import PeerServer
from Interwebs import Peer

from Interwebs.Protocols import Event

import tkinter as tk
import tkinter.ttk as ttk

import pickle
import time
import random

from collections import namedtuple



class ChatClient(object):

	'''
	Docstring goes here

	'''


	def __init__(self):
		
		'''
		Docstring goes here

		'''

		# Configurations
		self.size  = 480, 720
		self.debug = True

		# Create the window
		self.window = tk.Tk()
		# self.window.geometry('{width}x{height}'.format(width=self.size[0], height=self.size[1]))
		self.window.title('Chat')

		def onsubmit(ev):
			print('onsubmit')
			self.postEntry(self.write.get())

		# Create the interface
		self.write = ttk.Entry()
		self.write.grid(column=0, row=1)
		self.write.bind('<Return>', onsubmit)

		self.entryFrame = ttk.Frame() # width=self.size[0], height=self.size[1]-30
		self.entryFrame.grid(column=0, row=0)

		self.entries = []

		self.peer = Peer.Peer('localhost', 255, onreceive=lambda sender, data: self.addEntry(data), onconnect=lambda sender, data: None) #

		#
		self.window.mainloop()


	def postEntry(self, message):

		'''
		Docstring goes here

		'''

		self.log('Posting entry: {0}'.format(message))
		self.addEntry(message)
		self.peer.send(pickle.dumps(message))


	def addEntry(self, message):

		'''
		Docstring goes here

		'''

		self.log('Adding entry: {0}'.format(message))
		entry = ttk.Label(master=self.entryFrame, text=time.strftime('(%H:%M:%S) {0}', time.localtime()).format(message))
		entry.grid(column=0, row=len(self.entries))
		self.entries.append(entry)


	def log(self, msg, level=None):
		if self.debug: print(msg)