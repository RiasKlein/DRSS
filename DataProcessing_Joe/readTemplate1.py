###############################################################################
#																			  #
# readTemplate1.py															  #
#																			  #
#  Contains the reading procedure for UNCF donor data						  #
#  - Uses the '$' and RANGE_STR global variable to locate the start of donors #
#  - Uses the END_SEQ global variable to find the end of donors				  #
#																			  #
#	Written by: Joseph Bieselin				Spring 2016						  #
#																			  #
###############################################################################

import sys
from helpers import *

RANGE_STR = "and up" # used for donation amount retrieval, i.e. "$1,000,000 and up"
END_SEQ   = "and evening of stars" # used to signify the end of donors

# Unicode characters will be stripped from all lines
BULLET_UNICODE = '\xb7'
SPADE_UNICODE  = '\x0c'


def readTemplate1 ( rFileName, wfileName ):
	'''
	Opens read and write files for donor processing; returns False if Errors occur.
	Calls functions that will find donation amounts and corresponding donor names.
	The amounts and names will be read from the file with name: rfileName
	The amounts and names will be written to the file with name: wfileName
	
	The file with wfileName will have the following example output upon correct processing:
	---
	1000000
	abc
	def
	ghi
	500000
	jkl
	mno
	pqr
	250000
	stu
	vwx
	100000
	yz
	---
	The donation amount is followed by multiple lines of every donor that donated said amount.
	The donation amount is a lower bound for how much the donor donated, but is capped by the
	previous donation amount.
	'''

	try:
		rfile = open(rFileName, 'r')
	except IOError:
		print "IOError - opening read file."
		return False

	try:
		wfile = open(wfileName, 'w')
	except IOError:
		print "IOError - opening write file."
		return False

	try:
		findDonationStart( rfile )
	except:
		print "Error in findDonationStart function."
		rfile.close()
		wfile.close()
		return False

	try:
		lst = processDonors( rfile )
	except:
		print "Error in processDonors function."
		return False

	"""
	try:
		writeData( lst, wfile )
	except:
		print "Error in writeData function."
		return False
	"""
	writeData(lst, wfile)

	rfile.close()
	wfile.close()


def findDonationStart ( rfile ):
	'''
	Places rfile's file pointer at the beginning of the line that contains
	the first donation amount information.
	
	Example file format:
	---
	Some lines about some stuff that is cool
	but we don't care about for this system.
	This organization does amazing work and gets gifts from people.
	Corporations/Trusts/People...
	$1,000,000 and up
	donor_a
	donor_b
	$500,000 - $999,999
	donor_x
	donor_y
	donor_z
	---
	This will leave the rfile's file pointer at the line containing "$1,000,000 and up"
	'''

	while True:

		# Remember our starting file position to reset to when we find the starting donation amount
		lastFilePos = rfile.tell()

		line = rfile.readline().strip(BULLET_UNICODE + SPADE_UNICODE + ' \n')

		# If no donation info was found before the end of the file, return False
		if not line:
			return False

		# Reset the file pointer to the beginning of the line
		if dollarsAndUp( line, RANGE_STR) or dollarsRange( line ):
			rfile.seek(lastFilePos)
			return True


def pg():
	sys.stderr.write("GOOD\n")

def processDonors( rfile ):
	'''
	Loops through rfile and adds donations/donors to a lst.
	rfile's file pointer should point to the first line of donation amounts to store.
	
	Information added corresponds to a donation amount followed by donors
	that donated said amount. All such amounts and donors in rfile are processed.
	'''

	lst = []

	line = rfile.readline().strip(BULLET_UNICODE + SPADE_UNICODE + ' \n')

	# Start processing the donation/donor data
	while line:

		# End processing if END SEQUENCE is found in the line
		if line.lower().find(END_SEQ) != -1:
			break

		# Get the data amount that will be stored in wfile to show how much the donation was
		elif ( dollarsAndUp( line, RANGE_STR ) or dollarsRange( line ) ):
			# Get the lower bound of the donation amount
			dollars = dollarsAndUp( line, RANGE_STR )
			if not dollars:
				dollars = dollarsRange( line )

			lst.append(dollars)

		# If not the END, and not a donation amount, it is likely a donor name
		else:
			# Remove any possible asterisks at end of line and append donor to lst\
			lst.append(removeAsterisks( line ))


		# Get the next line for further processing
		line = rfile.readline().strip(BULLET_UNICODE + SPADE_UNICODE + ' \n')

	return lst


def writeData( lst, wfile ):
	'''
	lst contains donation values and donor names to be written to wfile separated by newlines.
	Elements in lst may be combined/modified/deleted or have other changes
	being made to it. These changes are for the purpose of cleaning up the
	data to be written to the output file.
	'''

	ignore_list = ["special events", "*Includes", "MAJOR", "My number one", "I need to", "James Mbyrukira", "Chair, Dep", "UNCF-member", "U N C F", "lists represent", "accurate listing"]
	
	merge_list = ["Company"]
	
	# Loop over lst and write the data to the file with newlines in between each
	for line in lst:
		if not line: break			# make sure we got something to work with
		line = str(line)			# make sure our line is a string
		
		# Presenting the UNCF String Immigration Service 
		keep_line = True			# assume we want this line
		
		# Check if the line contains unwanted "illegal" goods
		for word in ignore_list:
			if word in line:
				keep_line = False
		
		if (keep_line):
			wfile.write(line + "\n")

