###############################################################################
#																			  #
# helpers.py																  #
#																			  #
#	Contains functions to help with reading templates						  #
#																			  #
#	Written by: Joseph Bieselin				Spring 2016						  #
#																			  #
###############################################################################




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

	return string.rstrip('*' + ' ')
