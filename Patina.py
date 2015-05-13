#
# Patina
# ?
#
# Jonatan H Sundqvist
# May 12 2015
#

# TODO | - 
#        - 

# SPEC | -
#        -



from PyQt4 import QtGui
from sys import argv



def main():
  
	'''
	Docstring goes here

	'''

	app = QtGui.QApplication(argv)

	widget = QtGui.QWidget()
	widget.resize(700, 400)
	widget.move(30, 100)
	
	widget.setWindowTitle('Chat')
	# widget.setWindowIcon(QtGui.QIcon('.png'))

	widget.show()

	app.exec_()



if __name__ == '__main__':
	main()