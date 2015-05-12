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
		def __init__(self, name, x, y, size):
			self.name = name # Name as a string
			self.jumping = False #


			self.p = x+1j*y  # Position (m   : vector)
			self.v = 0+0j    # Velocity (m/s : vector)
			self.m = 1       # Mass     (kg  : scalar)
			self.f = {'gravity': 0+9.82j, 'normal': 0+9.82j} # Forces (N : vector)

			self.size = size # Size (m : vector)

		def velocity(self, v, add=False):
			self.v = self.v + v if add else v

		def bounds(self, normalise=lambda x: x):
			topleft     = self.p-self.size/2
			bottomright = self.p+self.size/2
			return  (normalise(topleft.real), normalise(topleft.imag), normalise(bottomright.real), normalise(bottomright.imag))

		def label(self, coords=False):
			return (self.p.real, self.p.imag-self.size.imag/2-10)

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
		self.player = Platformer.Player(name=random.choice(('Jonatan', 'Ali Baba', 'Ser Devon')),
			                            x=random.randint(20, self.size[0]-20),
			                            y=self.size[1]-self.groundlevel-30/2,
			                            size=18+30j)

		self.others = {} # Other players

		# Canvas
		self.canvas = tk.Canvas(width=self.size[0], height=self.size[1])
		self.ground = self.canvas.create_rectangle((0, self.size[1]-self.groundlevel, self.size[0], self.size[0]), fill='#45DE9F', width=0)
		self.player.visual = { 'body':    self.canvas.create_rectangle(self.player.bounds(normalise=int), fill='#FB00EC', width=0),
		                       'nametag': self.canvas.create_text(self.player.label(), text=self.player.name, anchor=tk.CENTER) }
		self.canvas.pack()

		# Animation
		self.running = False #
		self.FPS = 30        # Frames per second
		
		# Key bindings
		self.window.bind('<KeyPress-Left>',  lambda e: self.player.velocity(v=-90.0+0j, add=False))
		self.window.bind('<KeyPress-Right>', lambda e: self.player.velocity(v= 90.0+0j, add=False))
		
		self.window.bind('<KeyRelease-Left>',  lambda e: self.player.velocity(v=0+0j, add=False))
		self.window.bind('<KeyRelease-Right>', lambda e: self.player.velocity(v=0+0j, add=False))
		
		self.window.bind('<KeyRelease-p>', lambda e: self.play(toggle=True)) # Start the game when player presses spacebar

		#
		# self.peer = Peer.Peer('localhost', 255, onreceive=lambda data: updateRemotePlayers(data)) #

		#
		self.window.mainloop()


	def play(self, toggle=False):
		self.running = not self.running if toggle else True
		print('Game is now {0}.'.format(('paused', 'running')[self.running]))
		if self.running:
			self.tick() #


	def tick(self):

		'''
		Docstring goes here

		'''

		if not self.running:
			self.window.after(int(1000/self.FPS), lambda: self.tick())

		self.player.animate(1.0/self.FPS)
		self.canvas.coords(self.player.visual['body'], self.player.bounds(normalise=int))
		self.canvas.coords(self.player.visual['nametag'], self.player.label())
		self.notifyServer()

		self.window.after(int(1000/self.FPS), lambda: self.tick())


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