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



import platformer
import chat


# Sample programs
programs = {
	'chat':       lambda: chat.ChatClient(), #
	'platformer': lambda: platformer.Platformer(), #
	'': lambda: None
}



def main():

	'''
	Docstring goes here

	'''

	#
	# print('Which sample would you like to run?')
	# print('\n'.join('  [{0}] {1}'.format(n, sample) for n, sample in enumerate(programs.keys(), 1)))
	# programs[input('  Choose: ')]()
	programs['platformer']()



if __name__ == '__main__':
	main()