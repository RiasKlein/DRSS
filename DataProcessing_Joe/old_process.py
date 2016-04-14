################################################################################
# 									       #
# process.py								       #
# 									       #
#	Contains the data processing component of the DRSS 		       #
#	Usage:								       #
#		python process.py (filename to process)	(Template Code         #
#									       #
#	Created by: Joseph Bieselin                                            #
#									       #
################################################################################

import sys
#from findDollar import *
from readTemplate1 import *


'''HARDCODED FOR NOW TO TEST UNCF DATA'''
rfileName = "uncf.txt"
wfileName = "uncf_donors.txt"


# Settings
DEBUG = True		# Turn this off for release
T_CODE = -1			# Assume that there is no existing template
output_file_name = "out_template1.txt"

# If there is an extra input, check for the organization code
if len(sys.argv) > 2:
	T_CODE = int (sys.argv[2])

# Standard Operation of Data Processor
#	- Read through provided file
#	- Find donation amount & corresponding donors
#	- Output the relevant information to an output file
def main():
#	# If DEBUG mode is on, run findDollar on the provided filename
#	if (DEBUG):
#		findDollar (sys.argv[1])
#			
#	# First we open the file for reading
#	# The donor file should be provided as the first argument
#	try:
#		rfile = open (sys.argv[1], 'r')		# open the donor report for reading
#	except:
#		print "Error: Failed to open the specified file. Make sure that the file is in the current directory."
#		print "Usage: python process.py [filename to process]"
#		
#	# Open an output file to place relevant information
#	wfile = open (output_file_name, 'w')
#		
#	readTemplate0 (rfile, wfile)
#
#	# Close the files when we are done
#	rfile.close()
#	wfile.close()
#	
#	print "Data Processing: Complete"
    readTemplate1( rfileName, wfileName )
    
	
# Calling the main function
main()
	
