################################################################################
# 																			   #
# process.py																   #
# 																			   #
#	Contains the data processing component of the DRSS 						   #
#	Usage:																	   #
#		python process.py (filename to process)	(Template Code)			  	   #
#																			   #
#	Created by: Shunman Tse													   #
#																			   #
################################################################################

import sys
from findDollar import *
from readTemplate0 import readTemplate0
from readTemplate2 import readTemplate2

# Settings
DEBUG = True		# Turn this off for release
T_CODE = -1			# Assume that there is no existing template

# If there is an extra input, check for the organization code
if len(sys.argv) > 2:
	T_CODE = int (sys.argv[2])

# Standard Operation of Data Processor
#	- Read through provided file
#	- Find donation amount & corresponding donors
#	- Output the relevant information to an output file
def main():
	# If DEBUG mode is on, run findDollar on the provided filename
	if (DEBUG):
		findDollar (sys.argv[1])
			
	# First we open the file for reading
	# The donor file should be provided as the first argument
	try:
		rfile = open (sys.argv[1], 'r')		# open the donor report for reading
	except:
		print "Error: Failed to open the specified file. Make sure that the file is in the current directory."
		print "Usage: python process.py [filename to process] [template_code]"
		
	if (T_CODE == 0):
		readTemplate0(rfile)
	elif (T_CODE == 2):
		readTemplate2(rfile)
		
	#readTemplate2(rfile)

	# Close the files when we are done
	rfile.close()
	
	print "Data Processing: Complete"
	
# Calling the main function
main()
	

	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	

