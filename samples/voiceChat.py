#
# radio.py
# Voice broadcasting
#
# None
# May 24 2015
#

# TODO | - 
#        - 

# SPEC | -
#        -



import queue
import tkinter as tk
import pyaudio
import pickle
import threading

import base64

from Interwebs import PeerServer
from Interwebs import Peer



class VoiceChat(object):

	'''
	Docstring goes here

	'''

	def __init__(self):

		'''
		Docstring goes here

		'''

		#
		self.size = 450, 450

		#
		self.playing = True

		# Stream parameters
		self.CHUNKSIZE  = 1024  #
		self.WIDTH      = 2     # ?
		self.CHANNELS   = 2     # Number of channels
		self.SAMPLERATE = 44100 # Sample rate (samples per second)

		#
		self.pyaudio = pyaudio.PyAudio() #
		self.stream  = self.pyaudio.open(format=self.pyaudio.get_format_from_width(self.WIDTH),
			                             channels=self.CHANNELS,
			                             rate=self.SAMPLERATE,
			                             input=True,
			                             output=True,
			                             frames_per_buffer=self.CHUNKSIZE)

		#
		self.window = tk.Tk()
		self.window.geometry('{width}x{height}'.format(width=self.size[0], height=self.size[1]))
		self.window.title('Voice Chat')

		#
		self.outchunks = queue.Queue() #
		self.inchunks  = queue.Queue() #

		#
		self.peer = Peer.Peer('localhost', 12345, onreceive=lambda sender, data: self.inchunks.put(pickle.loads(base64.b64decode(data))), onconnect=lambda sender, data: None) #
# self.inchunks.put(pickle.loads(base64.b64decode(data)))
		self.micThread  = threading.Thread(target=lambda: self.record()).start()
		self.sendThread = threading.Thread(target=lambda: self.send()).start()
		self.playThread = threading.Thread(target=lambda: self.play()).start()

		
	def record(self):
		# TODO: This method is haunted
		# TODO: This method is very inefficient
		while True:
			if self.playing:
				self.outchunks.put(self.stream.read(self.CHUNKSIZE))


	def send(self):
		while True:
			self.peer.send(base64.b64encode(pickle.dumps(self.outchunks.get())))


	def play(self):

		'''
		Docstring goes here

		'''

		while True:
			self.stream.write(self.inchunks.get(), self.CHUNKSIZE)




def main():

	'''
	Docstring goes here

	'''

	app = VoiceChat()
	app.window.mainloop()



if __name__ == '__main__':
	main()