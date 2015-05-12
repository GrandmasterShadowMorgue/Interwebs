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
import time

import random



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

		self.peer = Peer.Peer('localhost', 255, onreceive=lambda data: self.addEntry(data)) #

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



class Platformer(object):

	'''
	Docstring goes here

	'''

	# TODO: Refactor (logic/graphics/network)
	# TODO: Separate coordinate system

	class Player(object):
		# TODO: Encapsulate updates (?)
		# TODO: Encapsulate graphical updates (?)
		def __init__(self, name, x, y):
			self.name = name # Name as a string
			self.jumping = False #

			self.p = x+1j*y  # Position (m   : vector)
			self.v = 0+0j    # Velocity (m/s : vector)
			self.m = 1       # Mass     (kg  : scalar)
			self.f = {'gravity': 0+9.82j, 'normal': 0+9.82j} # Forces (N : vector)

		def jump(self, v):
			self.v += v
			self.jumping = True
			# self.f['normal'] = 0+0j

		def animate(self, dt):
			self.p += self.v * dt # TODO: Proper physics/forces/collisions/etc.


	def __init__(self):

		'''
		Docstring goes here

		'''

		# Configurations
		self.size  = 720, 480
		self.debug = True

		# Create the window
		self.window = tk.Tk()
		self.window.geometry('{width}x{height}'.format(width=self.size[0], height=self.size[1]))
		self.window.title('Platformer')

		# World
		self.groundlevel = 40
		self.player = Player(random.choice(('Jonatan', 'Ali Baba', 'Ser Devon')), x=random.randint)

		# Canvas
		self.canvas = tk.Canvas(width=self.size[0], height=self.size[1])
		self.ground = self.canvas.create_rectangle((0, self.size[1]-groundlevel, self.size[0], self.size[0]), fill='#45DE9F', width=0)
		self.canvas.pack()

		#
		self.peer = Peer.Peer('localhost', 255, onreceive=lambda data: updateRemotePlayers(data)) #

		#
		self.window.mainloop()


	def tick(self):

		'''
		Docstring goes here

		'''

		self.notifyServer()


	def notifyServer(self):

		'''
		Docstring goes here

		'''

		pass


	def updateRemotePlayers(self, data):

		'''
		Docstring goes here

		'''

		pass



# Sample programs
programs = {
	'chat':       lambda: ChatClient(), #
	'platformer': lambda: Platformer(), #
	'': lambda: None
}



def main():

	'''
	Docstring goes here

	'''

	#
	programs['platformer']()



if __name__ == '__main__':
	main()