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

RANGE_STR = "and Above" # used for donation amount retrieval, i.e. "$1,000,000 and up"
MAX_STR	  = "Up to"		# used for donation amount retrieval, i.e. "Up to $9,999"
END_SEQ_1   = "Brookings strives for" 	# used to signify the end of donors
END_SEQ_2	= "STATEMENT OF ACTIVITIES"	# used to signify the end of donors
DONATION_AMOUNT = ">>> Donation Amount: %d"		# used for writing donation amounts to the output file

# Unicode characters will be stripped from all lines
BULLET_UNICODE = '\xb7'
SPADE_UNICODE  = '\x0c'
UNICODE_HYPHEN = '\x96'
UNICODE_COMMA_UNDER_LETTER = '\xb8'


def process ( rFileName, wfileName ):
	'''
	Opens read and write files for donor processing; returns a negative number if an error occurs.
	0 is returned if the function finishes without any errors (that are known anyway).
	
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
		return -1

	try:
		wfile = open(wfileName, 'w')
	except IOError:
		print "IOError - opening write file."
		return -2

	try:
		findDonationStart( rfile )
	except:
		print "Error in findDonationStart function."
		rfile.close()
		wfile.close()
		return -3

	try:
		lst = processDonors( rfile )
	except:
		print "Error in processDonors function."
		return -4

	try:
		writeData( lst, wfile )
	except:
		print "Error in writeData function."
		return -5

	rfile.close()
	wfile.close()

	return 0


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
	$1,000,000 and Above
	donor_a
	donor_b
	$500,000-$999,999
	donor_x
	donor_y
	donor_z
	---
	This will leave the rfile's file pointer at the line containing "$1,000,000 and up"
	'''

	while True:

		# Remember our starting file position to reset to when we find the starting donation amount
		lastFilePos = rfile.tell()

		line = rfile.readline().strip(BULLET_UNICODE + SPADE_UNICODE + UNICODE_COMMA_UNDER_LETTER + ' ' + '\n')

		# If no donation info was found before the end of the file, return False
		if not line:
			return False

		# Reset the file pointer to the beginning of the line
		if dollarsAndUp( line, RANGE_STR) or dollarsRange( line, UNICODE_HYPHEN ) or upToDollars( line, MAX_STR ):
			rfile.seek(lastFilePos)
			return True


def processDonors( rfile ):
	'''
	Loops through rfile and adds donations/donors to a lst.
	rfile's file pointer should point to the first line of donation amounts to store.
	
	Information added corresponds to a donation amount followed by donors
	that donated said amount. All such amounts and donors in rfile are processed.
	'''

	lst = []

	line = rfile.readline().strip(BULLET_UNICODE + SPADE_UNICODE + UNICODE_COMMA_UNDER_LETTER + ' ' + '\n')

	# Start processing the donation/donor data
	while line:

		# End processing if endSequence returns True
		if endSequence( line, [END_SEQ_1, END_SEQ_2] ):
			break

		# Get the data amount that will be stored in wfile to show how much the donation was
		elif ( dollarsAndUp( line, RANGE_STR ) or dollarsRange( line, UNICODE_HYPHEN ) or upToDollars( line, MAX_STR ) ):
			# Get the lower bound of the donation amount
			dollars = dollarsAndUp( line, RANGE_STR )
			if not dollars:
				dollars = dollarsRange( line, UNICODE_HYPHEN )
			if not dollars:
				# upToDollars returned the valid int which means the donations are capped by the return int
				# Just set dollars to 1 because the previous donation amount will be the known cap
				dollars = 1
			# One of the functions with DOLLARS returned a valid int, so make sure dollars contains that valid int

			lst.append(dollars)

		# If not the END, and not a donation amount, it is likely a donor name
		else:
			# Remove any possible asterisks at end of line and append donor to lst\
			lst.append(removeAsterisks( line ))


		# Get the next line for further processing
		line = rfile.readline().strip(BULLET_UNICODE + SPADE_UNICODE + UNICODE_COMMA_UNDER_LETTER + ' ' + '\n')

	return lst


def endSequence ( line, endSeqList ):
	'''
	Returns True if any element in endSeqList is contained in line; False otherwise.
	'''
	# Return True if one of the sequences in endSeqList is contained in line
	for seq in endSeqList:
		if seq.lower() in line.lower():
			return True

	return False


def writeData( lst, wfile ):
	'''
	lst contains donation values and donor names to be written to wfile separated by newlines.
	Elements in lst may be combined/modified/deleted or have other changes
	being made to it. These changes are for the purpose of cleaning up the
	data to be written to the output file.
	'''

	ignore_list = getIgnoreList()
	merge_list = getMergeList()

	# Loop over lst and write the data to the file with newlines in between each
	index = 0
	while index < len(lst):


		# Only the donation amounts are stored as ints
		if type(lst[index]) is int:
			# Place the donation amount integer into the formatted string for outputting
			line = DONATION_AMOUNT % lst[index]
			wfile.write(line + '\n')

		# Check the contents of the line
		else:		
			line = str(lst[index])			# get something and stringify it from the donor list

			# Presenting the UNCF String Immigration Service 
			keep_line = True			# assume we want this line

			# If the line is in ignore_list, we don't want to write it to the output file
			for word in ignore_list:
				if word in line:
					keep_line = False

			if (keep_line):
				# See if we need to merge two donor lines that should be together
				if index != (len(lst) - 1):
					# Not at the last element in lst so we can check the next element
					nextLine = str(lst[index + 1])
					for word in merge_list:
						# If nextLine is a word in merge_list, merge it with our current line
						if nextLine == word:
							line += ' ' + nextLine	# append the info that should have be together on one line
							index += 1				# increment index an extra time since the next element in lst is appended
							break					# break since something was merged already

				wfile.write(line + '\n')

		index += 1					# increment index to get the next donor


def getIgnoreList():
	'''Returns a list of combined ignore lists from all donor templates'''
	
	lst = []

	UNCF = ["special events", "*Includes", "MAJOR DONORS", "My number one", "I need to", "James Mbyrukira", "Chair, Dep", "UNCF-member", "U N C F", "lists represent", "accurate listing", "FOUNDATIONS", '"Education', "issue because", "other problem", " Former Sen.", "CORPORATE", "CAMPAIGNS", '"College', "while family", "remain", "make", "students to enroll", "even more", " The College Board Advocacy", "GROUPS", "UNIONS", "CHURCHES", "PUBLIC CAMPAIGNS", '"Better', "of every", "reform's", "a constituency", "business community", " Dr.", "INDIVIDUALS", '"We', "will out", "will be", "that every", "competitive education", "born to", " President", '"President', "nation.", "proportion", "HBCUs", "leadership", " U.S."] 
	BROOKINGS = []

	lst.extend(UNCF)
	lst.extend(BROOKINGS)

	return lst


def getMergeList():
	'''Returns a list of combined merge lists from all donor templates'''
	
	lst = []

	UNCF = ["Company", "Foundation", "Foundation, Inc.", "and Research", "Pharmaceutical, Inc.", "Charities Central", "Worldwide, Inc.", "Advertising, Inc.", "Division", "Insurance Company", "Indiana Central", "North Texas, Inc.", "Pictures, LLC", "Resources, LLC", "Flom, LLP", "Foundation, Inc", "Charitable Foundation", "Scholarship Fund, Inc.", "Memorial Fund", "Charity Fund", "Philanthropic Fund", "Family Foundation", "Cincinnati Foundation", "Community Foundation", "Giving Fund", "Sol G. Atlas Fund", "Fund III", "Educational Trust", "Fund", "Trust", "Connections Fund", "Headlee Trust", "Gift Campaign", "Corporate Campaign", 'Hope" Campaign', "Campaign", "Campaign", "Campaign for the Community", "Employee Giving", "Combined Campaign", "Beach County", "Housing Authority", "Transportation Authority", "Employee Resource Group", "Combined Federal Campaign", "Municipal Campaign", "Services", "Employees Campaign", "Combined Federal Campaign"]
	BROOKINGS = []

	lst.extend(UNCF)
	lst.extend(BROOKINGS)

	return lst