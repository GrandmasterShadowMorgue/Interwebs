#
# platformer.py
# ?
#
# Jonatan H Sundqvist
# May 13 2015
#

# TODO | - 
#        - 

# SPEC | -
#        -



from Interwebs import Peer
from Interwebs.Protocols import Event

import tkinter as tk
import tkinter.ttk as ttk

import pickle
import time
import random

from collections import namedtuple



PlayerData = namedtuple('PlayerData', 'name position size fill') #



class Platformer(object):

	'''
	Docstring goes here

	'''

	# TODO: Refactor (logic/graphics/network)
	# TODO: Separate coordinate system (world/screen)


	class Player(object):
		
		def __init__(self, name, position, size, fill, canvas, transform, arrow=tk.NORMAL):
			self.name = name                                                # Name as a string
			self.body = Platformer.Body(p=position, size=size, v=0+0j, m=1) #

			self.fill = fill #
			self.visuals = self.createVisuals(canvas, arrow, transform)

		def render(self, canvas, transform):
			# TODO: Cache transforms
			canvas.coords(self.visuals['body'],        self.body.bounds(transform=transform, normalise=int))
			canvas.coords(self.visuals['arrow'],       self.arrow(length=0.18, pady=0.20, transform=transform, normalise=int))
			canvas.coords(self.visuals['nametag'],     self.label(pady=0.12, transform=transform, normalise=int))
			canvas.itemconfig(self.visuals['nametag'], text='{name}'.format(name=self.name))

		def label(self, pady, transform, normalise=lambda x: x):
			anchor = transform(self.body.p.real+(self.body.p.imag+self.body.size.imag/2+pady)*1j) # TODO: Don't hardcode distance (10)
			return (normalise(anchor.real), normalise(anchor.imag))

		def arrow(self, length, pady, transform, normalise=lambda x: x):
			begin = transform(self.body.p.real+(self.body.p.imag+self.body.size.imag/2+length+pady)*1j) #
			end   = transform(self.body.p.real+(self.body.p.imag+self.body.size.imag/2+pady)*1j)        #
			return (normalise(begin.real), normalise(begin.imag), normalise(end.real), normalise(end.imag))

		def createVisuals(self, canvas, arrow, transform):
			return { 'body':    canvas.create_rectangle(self.body.bounds(transform=transform, normalise=int), fill=self.fill, width=0),
		             'nametag': canvas.create_text(self.label(pady=0.12, transform=transform, normalise=int), text=self.name, anchor=tk.CENTER, fill='#C9C9C9'),
		             'arrow':   canvas.create_line(self.arrow(length=0.18, pady=0.20, transform=transform, normalise=int), width=14, fill='#89DF0D', state=arrow, arrow='last') }


	class Body(object):
		# TODO: Encapsulate updates (?)
		# TODO: Encapsulate graphical updates (?)
		# TODO: How to pickle (?)
		# TODO: Use namedtuple or class for bounds and points
		# TODO: Check arguments, testing (...)
		# TODO: Other shapes, proper collisions, bbox object (?)
		# TODO: Other physical properties (eg. restitution)
		def __init__(self, p, size, v=0+0j, m=1.0):
			# TODO: Check interfaces instead (?)
			assert all(isinstance(attribute, domain) for domain, attribute in ((complex, p), (complex, size), (complex, v), ((int, float), m))) #
			self.jumping = False #

			self.p = p      # Position (m   : vector)
			self.v = v      # Velocity (m/s : vector)
			self.m = m      # Mass     (kg  : scalar)
			self.f = {'gravity': 0-9.82j, 'normal': 0+9.82j} # Forces (N : vector)

			self.size = size # Size (m : vector)

		def velocity(self, v, add=False):
			# print('Setting velocity')
			self.v = self.v + v if add else v

		def bounds(self, transform, normalise=lambda x: x):
			topleft     = transform(self.p-self.size/2)
			bottomright = transform(self.p+self.size/2)
			return (normalise(topleft.real), normalise(topleft.imag), normalise(bottomright.real), normalise(bottomright.imag))
			# return  transform(topleft)+transform(bottomright)*1j


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
		self.window.title('Platformer (paused)') #

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
		self.player = Platformer.Player(name=random.choice(('Jonatan', 'Ali Baba', 'Ser Devon', 'Jayant', 'Don Quixote')),
			                            # TODO: Explicit conversion to world coords
			                            position=self.pointToWorldCoords(random.uniform(20, self.size[0]-20)+(self.size[1]-self.groundlevel-30/2)*1j),
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
		# TODO: Refactor
		self.window.bind('<KeyPress-Left>',  lambda e: self.player.body.velocity(v=-1.2-self.player.body.v.real, add=True))
		self.window.bind('<KeyPress-Right>', lambda e: self.player.body.velocity(v= 1.2-self.player.body.v.real, add=True))
		
		self.window.bind('<KeyRelease-Left>',  lambda e: self.player.body.velocity(v=-self.player.body.v.real, add=True))
		self.window.bind('<KeyRelease-Right>', lambda e: self.player.body.velocity(v=-self.player.body.v.real, add=True))
		
		self.window.bind('<space>', lambda e: self.player.body.jump(3.0j)) # TODO: No double-jumping

		self.window.bind('<KeyRelease-p>', lambda e: self.play(toggle=True)) # Start the game when player presses spacebar

		# 
		# TODO: Refactor
		self.peer = Peer.Peer(('localhost', '192.168.1.88')[0], 12345,
			onreceive=lambda sender, data: self.updateRemotePlayer(sender, data),
			onconnect=lambda sender, data: self.addNewPlayer(sender, data),
			onauthenticated=lambda ID: self.peer.send(data=self.serializePlayer(self.player), event=Event.Connect),
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
		self.window.title('Platformer ({state})'.format(state=('paused', 'running')[self.running]))
		if self.running:
			self.tick() #


	def tick(self):

		'''
		Docstring goes here

		'''

		if not self.running:
			#self.window.after(int(1000/self.FPS), lambda: self.tick())
			return

		past = self.player.body.animate(1.0/self.FPS, self.pointToWorldCoords((self.size[1]-self.groundlevel)*1j).imag)
		self.player.render(self.canvas, transform=lambda p: self.pointToScreenCoords(p, int))

		for other in self.others.values():
			other.render(self.canvas, transform=lambda p: self.pointToScreenCoords(p, int))

		if past != self.player.body.p:
			self.notifyServer()

		self.window.after(int(1000/self.FPS), lambda: self.tick())


	def addNewPlayer(self, ID, data):

		'''
		Docstring goes here

		'''

		print('Adding new player {0}: {1}'.format(ID, data))

		# TODO: Use namedtuple instead (?)
		# data.name, data.p.real, data.p.imag, self.size, self.canvas
		# self, name, position, size, fill, canvas, transform, arrow=tk.NORMAL
		self.others[ID] = self.loadPlayer(data) #

		# self.others[ID].visuals = self.others[ID].createVisuals(self.canvas)


	def removePlayer(self, ID):

		'''
		Docstring goes here

		'''
		
		#
		try:
			player = self.others[ID] # Player to be removed (he has become a nuisance)
			print('Removing player {0} ({1})'.format(ID, player.name))
			for part in player.visuals.values():
				self.canvas.delete(part)
			del self.others[ID]
		except KeyError as e:
			print('Cannot remove non-existing player {0}'.format(ID))


	def serializePlayer(self, player):

		'''
		Returns a pickled tuple with all the information necessary to reconstruct the given player

		'''

		return pickle.dumps(PlayerData(player.name, player.body.p, player.body.size, player.fill))


	def loadPlayer(self, data):

		'''
		Accepts a PlayerData tuple and returns a newly constructed player object (without an arrow)

		'''

		return Platformer.Player(data.name, data.position, data.size, data.fill, self.canvas, transform=lambda p: self.pointToScreenCoords(p, int), arrow=tk.HIDDEN)


	def notifyServer(self):

		'''
		Docstring goes here

		'''

		# TODO: Optimise (eg. no updates when player isn't moving)
		self.peer.send(pickle.dumps(self.player.body.p))


	def updateRemotePlayer(self, ID, data):

		'''
		Docstring goes here

		'''

		# print('\nUpdating remote player ({ID}, {data})\n'.format(ID=ID, data=data))
		self.others[ID].body.p = data #



def main():

	'''
	Docstring goes here

	'''

	app = Platformer()



if __name__ == '__main__':
	main()