###############################################################################
#																			  #
# process.py																  #
#																			  #
#	Processing template for UNCF											  #
#																			  #
#	Written by: Joseph Bieselin				Spring 2016						  #
#																			  #
###############################################################################

from sys import argv
from process import process


def readTemplate():

	# 3 inputs: 1) script name, 2) input text file to read, 3) output text file to write to
	if len(argv) != 3:
		print "Error - not enough inputs"
		exit(1)

	rfileName = argv[1]
	wfileName = argv[2]

	code = process( rfileName, wfileName )

	# If process returns a negative code, there was an error
	if code < 0:
		print "There was an error in the system..."
		exit(1)
