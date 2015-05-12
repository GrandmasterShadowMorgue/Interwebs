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

from Protocols import Event



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



class Platformer(object):

	'''
	Docstring goes here

	'''

	# TODO: Refactor (logic/graphics/network)
	# TODO: Separate coordinate system

	class Player(object):
		# TODO: Encapsulate updates (?)
		# TODO: Encapsulate graphical updates (?)
		# TODO: How to pickle (?)
		def __init__(self, name, x, y, size, fill, canvas, arrow=tk.NORMAL):
			self.name = name # Name as a string
			self.jumping = False #

			self.p = x+1j*y  # Position (m   : vector)
			self.v = 0+0j    # Velocity (m/s : vector)
			self.m = 1       # Mass     (kg  : scalar)
			self.f = {'gravity': 0+9.82j, 'normal': 0+9.82j} # Forces (N : vector)

			self.size = size # Size (m : vector)

			self.fill = fill #
			self.visuals = self.createVisuals(canvas, arrow)

		def velocity(self, v, add=False):
			self.v = self.v + v if add else v

		def bounds(self, normalise=lambda x: x):
			topleft     = self.p-self.size/2
			bottomright = self.p+self.size/2
			return  (normalise(topleft.real), normalise(topleft.imag), normalise(bottomright.real), normalise(bottomright.imag))

		def label(self, coords=False, normalise=lambda x: x):
			return (normalise(self.p.real), normalise(self.p.imag-self.size.imag/2-10)) # TODO: Don't hardcode distance (10)

		def arrow(self, length, pady):
			return (self.p.real, self.p.imag-self.size.imag/2-length-pady, self.p.real, self.p.imag-self.size.imag/2-pady)

		def jump(self, v):
			self.v += v
			self.jumping = True
			# self.f['normal'] = 0+0j

		def animate(self, dt):
			past = self.p
			self.p += self.v * dt # TODO: Proper physics/forces/collisions/etc.
			return past

		def render(self, canvas):
			canvas.coords(self.visuals['body'], self.bounds(normalise=int))
			canvas.coords(self.visuals['nametag'], self.label())
			canvas.itemconfig(self.visuals['nametag'], text='{name} {pos}'.format(name=self.name, pos=self.p))
			canvas.coords(self.visuals['arrow'], self.arrow(length=18, pady=25+8))

		def createVisuals(self, canvas, arrow):
			return { 'body':    canvas.create_rectangle(self.bounds(normalise=int), fill=self.fill, width=0),
		             'nametag': canvas.create_text(self.label(), text=self.name, anchor=tk.CENTER, fill='#C9C9C9'),
		             'arrow':   canvas.create_line(self.arrow(length=18, pady=25+8), width=14, fill='#89DF0D', state=arrow, arrow='last') }


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

		# Canvas
		self.canvas = tk.Canvas(width=self.size[0], height=self.size[1])
		self.ground = self.canvas.create_rectangle((0, self.size[1]-self.groundlevel, self.size[0], self.size[0]), fill='#45DE9F', width=0)
		self.canvas.pack()

		# Players
		self.player = Platformer.Player(name=random.choice(('Jonatan', 'Ali Baba', 'Ser Devon', 'Jayant')),
			                            x=random.randint(20, self.size[0]-20),
			                            y=self.size[1]-self.groundlevel-30/2,
			                            size=18+30j,
			                            fill=random.choice(('#F35678', '#FB00EC', '#FF8C69', '#EED5D2', '#71C671', '#5E2612', '#DAA520', '#9ACD32')),
			                            canvas=self.canvas)

		self.others = {} # Other players

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
		self.peer = Peer.Peer(('localhost', '192.168.1.88')[0], 12345, onreceive=lambda sender, data: self.updateRemotePlayer(sender, data),
		                                        onconnect=lambda sender, data: self.addNewPlayer(sender, data),
		                                        onauthenticated=lambda ID: self.peer.send(data=pickle.dumps((self.player.name, self.player.p, self.player.size, self.player.fill)),
		                                                                                  event=Event.Connect)) #

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

		past = self.player.animate(1.0/self.FPS)
		self.player.render(self.canvas)

		for other in self.others.values():
			other.render(self.canvas)

		if past != self.player.p:
			self.notifyServer()

		self.window.after(int(1000/self.FPS), lambda: self.tick())


	def addNewPlayer(self, ID, data):

		'''
		Docstring goes here

		'''

		print('Adding new player {0}: {1}'.format(ID, data))

		# TODO: Use namedtuple instead (?)
		# data.name, data.p.real, data.p.imag, self.size, self.canvas
		self.others[ID] = Platformer.Player(data[0], data[1].real, data[1].imag, data[2], data[3], self.canvas, tk.HIDDEN)

		# self.others[ID].visuals = self.others[ID].createVisuals(self.canvas)


	def notifyServer(self):

		'''
		Docstring goes here

		'''

		# TODO: Optimise (eg. no updates when player isn't moving)
		self.peer.send(pickle.dumps(self.player.p))


	def updateRemotePlayer(self, ID, data):

		'''
		Docstring goes here

		'''

		print('\nUpdating remote player ({ID}, {data})\n'.format(ID=ID, data=data))
		self.others[ID].p = data #



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