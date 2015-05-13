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

from Protocols import Event

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



class Platformer(object):

	'''
	Docstring goes here

	'''

	# TODO: Refactor (logic/graphics/network)
	# TODO: Separate coordinate system (world/screen)

	class Player(object):
		# TODO: Encapsulate updates (?)
		# TODO: Encapsulate graphical updates (?)
		# TODO: How to pickle (?)
		# TODO: Use namedtuple or class for bounds and points
		def __init__(self, name, x, y, size, fill, canvas, transform, arrow=tk.NORMAL):
			self.name = name     # Name as a string
			self.jumping = False #

			self.p = x+1j*y  # Position (m   : vector)
			self.v = 0+0j    # Velocity (m/s : vector)
			self.m = 1       # Mass     (kg  : scalar)
			self.f = {'gravity': 0+9.82j, 'normal': 0+9.82j} # Forces (N : vector)

			self.size = size # Size (m : vector)

			self.fill = fill #
			self.visuals = self.createVisuals(canvas, arrow, transform)

		def velocity(self, v, add=False):
			# print('Setting velocity')
			self.v = self.v + v if add else v

		def bounds(self, transform, normalise=lambda x: x):
			topleft     = transform(self.p-self.size/2)
			bottomright = transform(self.p+self.size/2)
			return (normalise(topleft.real), normalise(topleft.imag), normalise(bottomright.real), normalise(bottomright.imag))
			# return  transform(topleft)+transform(bottomright)*1j

		def label(self, pady, transform, normalise=lambda x: x):
			anchor = transform(self.p.real+(self.p.imag+self.size.imag/2+pady)*1j) # TODO: Don't hardcode distance (10)
			return (normalise(anchor.real), normalise(anchor.imag))

		def arrow(self, length, pady, transform, normalise=lambda x: x):
			begin = transform(self.p.real+(self.p.imag+self.size.imag/2+length+pady)*1j) #
			end   = transform(self.p.real+(self.p.imag+self.size.imag/2+pady)*1j)        #
			return (normalise(begin.real), normalise(begin.imag), normalise(end.real), normalise(end.imag))

		def jump(self, v):
			if not self.jumping:
				self.v += v
				self.jumping = True
				# self.f['normal'] = 0+0j

		def integrate(self, dt, p, v, a):
			return (v*dt + (1/2)*a*dt**2)

		def animate(self, dt, groundlevel):
			# TODO: Encapsulate collisions (?)
			past = self.p
			# self.p += self.v * dt # TODO: Proper physics/forces/collisions/etc.
			a = -9.82j if self.jumping else 0
			self.p += self.integrate(dt, self.p.real, self.v.real, a.real)    # Horizontal motion (self.a.real)
			self.p += self.integrate(dt, self.p.imag, self.v.imag, a.imag)*1j # Vertical motion
			self.v += a*dt

			# TODO: Don't hardcode groundlevel and canvas height
			onground = groundlevel + self.size.imag/2 #

			if self.jumping and (self.v.imag < 0) and (self.p.imag <= onground):
				self.p = self.p.real+onground*1j
				self.v = self.v.real
				self.jumping = False

			return past

		def render(self, canvas, transform):
			canvas.coords(self.visuals['body'], self.bounds(transform=transform, normalise=int))
			canvas.coords(self.visuals['nametag'], self.label(pady=0.12, transform=transform, normalise=int))
			canvas.itemconfig(self.visuals['nametag'], text='{name}'.format(name=self.name))
			canvas.coords(self.visuals['arrow'], self.arrow(length=0.18, pady=0.20, transform=transform, normalise=int))

		def createVisuals(self, canvas, arrow, transform):
			return { 'body':    canvas.create_rectangle(self.bounds(transform=transform, normalise=int), fill=self.fill, width=0),
		             'nametag': canvas.create_text(self.label(pady=0.12, transform=transform, normalise=int), text=self.name, anchor=tk.CENTER, fill='#C9C9C9'),
		             'arrow':   canvas.create_line(self.arrow(length=0.18, pady=0.20, transform=transform, normalise=int), width=14, fill='#89DF0D', state=arrow, arrow='last') }


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
		self.coordinatesystem = namedtuple('CoordinateSystem', 'scaling origin')(100-100j, (0.0+self.size[1])/100 * 1j) # TODO: Document coordinate system internals

		# Canvas
		self.canvas = tk.Canvas(width=self.size[0], height=self.size[1])
		self.ground = self.canvas.create_rectangle((0, self.size[1]-self.groundlevel, self.size[0], self.size[0]), fill='#45DE9F', width=0)
		self.canvas.pack()

		# UI
		self.mousecoords = self.canvas.create_text((5, 5), text='Screen (x={0:.02f}, y={1:.02f}) | World (x={2:.02f}, y={3:.02f})', anchor=tk.NW)
		self.canvas.bind('<Motion>', lambda e: self.canvas.itemconfig(self.mousecoords, text='Screen {0:.02f} | World {1:.02f}'.format(e.x+e.y*1j, self.pointToWorldCoords(e.x+e.y*1j))))

		# Players
		self.player = Platformer.Player(name=random.choice(('Jonatan', 'Ali Baba', 'Ser Devon', 'Jayant')),
			                            x=random.uniform(1.0, 3.5-1.0), # TODO: Explicit conversion to world coords
			                            y=self.pointToWorldCoords(0+(self.size[1]-self.groundlevel-30/2)*1j).imag,
			                            size=0.15+0.32j, # 18+30j,
			                            fill=random.choice(('#F35678', '#FB00EC', '#FF8C69', '#EED5D2', '#71C671', '#5E2612', '#DAA520', '#9ACD32')),
			                            canvas=self.canvas,
			                            transform=lambda p: self.pointToScreenCoords(p, int),
			                            arrow=tk.NORMAL)

		self.others = {} # Other players

		# Animation
		self.running = False #
		self.FPS = 30        # Frames per second
		
		# Key bindings
		self.window.bind('<KeyPress-Left>',  lambda e: self.player.velocity(v=-1.2-self.player.v.real, add=True))
		self.window.bind('<KeyPress-Right>', lambda e: self.player.velocity(v= 1.2-self.player.v.real, add=True))
		
		self.window.bind('<KeyRelease-Left>',  lambda e: self.player.velocity(v=-self.player.v.real, add=True))
		self.window.bind('<KeyRelease-Right>', lambda e: self.player.velocity(v=-self.player.v.real, add=True))
		
		self.window.bind('<space>', lambda e: self.player.jump(3.0j)) # TODO: No double-jumping

		self.window.bind('<KeyRelease-p>', lambda e: self.play(toggle=True)) # Start the game when player presses spacebar

		#
		self.peer = Peer.Peer(('localhost', '192.168.1.88')[0], 12345, onreceive=lambda sender, data: self.updateRemotePlayer(sender, data),
		                                        onconnect=lambda sender, data: self.addNewPlayer(sender, data),
		                                        onauthenticated=lambda ID: self.peer.send(data=pickle.dumps((self.player.name, self.player.p, self.player.size, self.player.fill)),
		                                                                                  event=Event.Connect),
		                                        ondisconnect=lambda ID: self.removePlayer(ID)) #

		#
		self.window.mainloop()


	def pointToScreenCoords(self, point, normalise=lambda x: x):
		# TODO: Rename (?)
		# TODO: Allow X origin offset (✓)
		origin  = self.coordinatesystem.origin
		scaling = self.coordinatesystem.scaling

		x = (point.real-origin.real)*scaling.real
		y = (point.imag-origin.imag)*scaling.imag

		return normalise(x)+normalise(y)*1j
		# return (normalise(x), normalise(y))


	def pointToWorldCoords(self, point, normalise=lambda x: x):
		# TODO: Rename (?)
		origin  = self.coordinatesystem.origin
		scaling = self.coordinatesystem.scaling

		x = (point.real/scaling.real)+origin.real
		y = (point.imag/scaling.imag)+origin.imag

		return normalise(x)+normalise(y)*1j
		# return (normalise(x), normalise(y))


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
			#self.window.after(int(1000/self.FPS), lambda: self.tick())
			return

		past = self.player.animate(1.0/self.FPS, self.pointToWorldCoords((self.size[1]-self.groundlevel)*1j).imag)
		self.player.render(self.canvas, transform=lambda p: self.pointToScreenCoords(p, int))

		for other in self.others.values():
			other.render(self.canvas, transform=lambda p: self.pointToScreenCoords(p, int))

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
		self.others[ID] = Platformer.Player(data[0], data[1].real, data[1].imag, data[2], data[3], self.canvas, lambda p: self.pointToScreenCoords(p, int), tk.HIDDEN)

		# self.others[ID].visuals = self.others[ID].createVisuals(self.canvas)


	def removePlayer(self, ID):

		'''
		Docstring goes here

		'''
		
		#	
		player = self.others[ID] # Player to be removed (he has become a nuisance)
		for part in player.visuals.values():
			self.canvas.delete(part)
		del self.others[ID]


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

		# print('\nUpdating remote player ({ID}, {data})\n'.format(ID=ID, data=data))
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