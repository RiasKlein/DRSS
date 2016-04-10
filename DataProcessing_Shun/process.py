################################################################################
# 																			   #
# process.py																   #
# 																			   #
#	Contains the data processing component of the DRSS 						   #
#	Usage:																	   #
#		python process.py (filename to process)	(-d)						   #
#																			   #
#	Created by: Shunman Tse													   #
################################################################################

import sys
from findDollar import *

# getDolarValue
# Extracts the integer value of the dollar value mentioned in the provided line
# That is, we will convert $1,000,000 to 1000000
# This value is returned at the end of the function
def getDollarValue ( line ):
	print (line) # WARNING: Placeholder, not the final function

# Settings
DEBUG = False

# Check for the extra inputs (if any)
if len(sys.argv) > 2:
	if sys.argv[2] == "-d":		# Turn on DEBUG mode if option -d is provided
		DEBUG = True

# Standard Operation of Data Processor
#	- Read through provided file
#	- Find donation amount & corresponding donors
#	- Output the relevant information to an output file
def main():
	# If DEBUG mode is on, run findDollar on the provided filename
	if (DEBUG):
		print "DEBUG: Running findDollar"
		findDollar (sys.argv[1])
		print "DEBUG: findDollar completed successfully"
	
	# First we open the file for reading
	# The donor file should be provided as the first argument
	try:
		rfile = open (sys.argv[1], 'r')		# open the donor report for reading
	except:
		print "Error: Failed to open the specified file. Make sure that the file is in the current directory."
		print "Usage: python process.py [filename to process]"
	
	# Open an output file to place relevant information
	wfile = open ("out_process.txt", 'w')
	
	# Reading through the donor file 
	while True:
		line = rfile.readline()		# read in a line from the donor report
		if not line: break			# stop reading when we reach the end of the report
		line.rstrip ('\n')			# get rid of newline characters at end of the line 
		
		# When we find a line with a '$' symbol, we must get the amount that is listed
		if '$' in line and "AND ABOVE" in line:				
			getDollarValue(line)
	
	# Close the files when we are done
	rfile.close()
	wfile.close()
	
# Calling the main function
main()
	

	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	

