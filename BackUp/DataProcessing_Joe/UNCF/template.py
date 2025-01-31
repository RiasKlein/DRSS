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






###############################################################################
#																			  #
# UNCF template																  #
#																			  #
#  Contains the reading procedure for UNCF donor data						  #
#  - Uses the '$' and RANGE_STR global variable to locate the start of donors #
#  - Uses the END_SEQ global variable to find the end of donors				  #
#																			  #
#	Written by: Joseph Bieselin				Spring 2016						  #
#																			  #
###############################################################################


RANGE_STR = "and up" # used for donation amount retrieval, i.e. "$1,000,000 and up"
END_SEQ   = "an evening of stars" # used to signify the end of donors
DONATION_AMOUNT = ">>> Donation Amount: %d"		# used for writing donation amounts to the output file

# Unicode characters will be stripped from all lines
BULLET_UNICODE = '\xb7'
SPADE_UNICODE  = '\x0c'


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

	ignore_list = ["special events", "*Includes", "MAJOR DONORS", "My number one", "I need to", "James Mbyrukira", "Chair, Dep", "UNCF-member", "U N C F", "lists represent", "accurate listing", "FOUNDATIONS", '"Education', "issue because", "other problem", " Former Sen.", "CORPORATE", "CAMPAIGNS", '"College', "while family", "remain", "make", "students to enroll", "even more", " The College Board Advocacy", "GROUPS", "UNIONS", "CHURCHES", "PUBLIC CAMPAIGNS", '"Better', "of every", "reform's", "a constituency", "business community", " Dr.", "INDIVIDUALS", '"We', "will out", "will be", "that every", "competitive education", "born to", " President", '"President', "nation.", "proportion", "HBCUs", "leadership", " U.S."] 
	
	merge_list = ["Company", "Foundation", "Foundation, Inc.", "and Research", "Pharmaceutical, Inc.", "Charities Central", "Worldwide, Inc.", "Advertising, Inc.", "Division", "Insurance Company", "Indiana Central", "North Texas, Inc.", "Pictures, LLC", "Resources, LLC", "Flom, LLP", "Foundation, Inc", "Charitable Foundation", "Scholarship Fund, Inc.", "Memorial Fund", "Charity Fund", "Philanthropic Fund", "Family Foundation", "Cincinnati Foundation", "Community Foundation", "Giving Fund", "Sol G. Atlas Fund", "Fund III", "Educational Trust", "Fund", "Trust", "Connections Fund", "Headlee Trust", "Gift Campaign", "Corporate Campaign", 'Hope" Campaign', "Campaign", "Campaign", "Campaign for the Community", "Employee Giving", "Combined Campaign", "Beach County", "Housing Authority", "Transportation Authority", "Employee Resource Group", "Combined Federal Campaign", "Municipal Campaign", "Services", "Employees Campaign", "Combined Federal Campaign"]

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






###############################################################################
#																			  #
#				helpers below originally written for UNCF					  #
#																			  #
###############################################################################


def dollarsAndUp ( line, RANGE_STR ):
	'''Returns the DOLLARS amount in a "DOLLARS and up" line; False otherwise.'''

	# Split the line up by whitespace to search for a DOLLARS amount and RANGE_STR
	list = line.strip().split()

	# Get the length of RANGE_STR (to be used for line checking)
	lengthRangeStr = len(RANGE_STR.split())

	# line was split by whitespace and placed into list
	# list needs to contain at least 1 element for the DOLLARS amount plus
	#   the number of elements that RANGE_STR comprises
	# For example:
	# DOLLARS = "$1,000,000", RANGE_STR = "and up"
	# len(list) should be at least 3 elements; 1 for DOLLARS + 2 for RANGE_STR
	if len(list) < lengthRangeStr + 1:
		return False

	dollars = list[0]
	dollars = getDollarAmount( dollars ) # get the integer value of DOLLARS
	# If dollars was not a dollar amount, return False
	if not dollars:
		return False

	# RANGE_STR should be contained within elements 1 and 2 of the list
	lineRangeStr = list[1].strip() + ' ' + list[2].strip()
	# If RANGE_STR cannot be found, return False
	if lineRangeStr.find(RANGE_STR) == -1:
		return False

	return dollars


def dollarsRange ( line ):
	'''Returns the smaller DOLLARS amount in a "SMALLER_DOLLARS - LARGER_DOLLARS" line; False otherwise.'''

	# Split the line up by whitespace to search for the two DOLLARS amounts
	list = line.strip().split()

	# list should be at least 3 elements due to the format of the line being checked for
	# SMALLER_DOLLARS, -, LARGER_DOLLARS each should comprise of 1 element
	# NOTE: hypens are not recognized as a searchable element in uncf.txt for donation ranges
	# Example format:
	# list = ["SMALLER_DOLLARS", "-", "LARGERS_DOLLARS"]
	if len(list) < 3:
		return False

	amount1 = list[0]
	amount1 = getDollarAmount( amount1 ) # get the integer value of SMALLER_DOLLARS

	amount2 = list[2]
	amount2 = getDollarAmount( amount2 ) # get the integer value of LARGER_DOLLARS

	# If amount1 or amount2 were not valid dollar amounts, return False
	if (not amount1) or (not amount2):
		return False

	# Return the integer represenation of SMALLER_DOLLARS
	return amount1


def getDollarAmount ( dollars ):
	'''Returns an interger representation of dollars; False otherwise.'''

	dollars = dollars.split('$')
	# dollars did not contain a dollar sign (so it is not a dollar amount), return False
	if len(dollars) == 1:
		return False

	# Example format:
	# dollars = ["", "1,000,000"]
	dollarAmount = dollars[1]

	# Remove all commas in the dollar amount
	noCommaDollarAmount = dollarAmount.replace(',', '')
	# If there were no commas, then it was not a dollar amount so return False
	if noCommaDollarAmount == dollarAmount:
		return False

	try:
		intDollarAmount = int(noCommaDollarAmount)
	except ValueError:
		print "In getDollarAmount: Error converting to int"
		return False

	return intDollarAmount


def removeAsterisks ( string ):
	'''
	Returns the passed in string with '*' and ' ' removed starting from the right side.
	Once any character that isn't an asterisk or space is hit, removal stops.
	'''

	return string.strip('*' + ' ')


