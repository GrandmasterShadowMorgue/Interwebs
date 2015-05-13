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