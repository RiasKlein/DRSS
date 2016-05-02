###############################################################################
#																			  #
#				helpers below originally written for Brookings				  #
#																			  #
###############################################################################


def dollarsAndUp ( line, rangeStr ):
	'''Returns the DOLLARS amount in a "DOLLARS and up" line; False otherwise.'''

	# Split the line up by whitespace to search for a DOLLARS amount and rangeStr
	lst = line.strip().split()

	# Get the length of rangeStr (to be used for line checking)
	lengthRangeStr = len(rangeStr.split())

	# line was split by whitespace and placed into lst
	# lst needs to contain at least 1 element for the DOLLARS amount plus
	#   the number of elements that rangeStr comprises
	# For example:
	# DOLLARS = "$1,000,000", rangeStr = "and up"
	# len(lst) should be at least 3 elements; 1 for DOLLARS + 2 for rangeStr
	if len(lst) < lengthRangeStr + 1:
		return False

	dollars = lst[0]
	dollars = getDollarAmount( dollars ) # get the integer value of DOLLARS
	# If dollars was not a dollar amount, return False
	if not dollars:
		return False

	# rangeStr should be contained within elements 1 and 2 of the lst
	lineRangeStr = lst[1].strip() + ' ' + lst[2].strip()
	# If rangeStr cannot be found, return False
	if lineRangeStr.find(rangeStr) == -1:
		return False

	return dollars


def upToDollars( line, maxStr ):
	'''Returns the DOLLARS amount in "Up to DOLLARS" line; False otherwise.'''

	# Split the line up by whitespace to search for a DOLLARS amount and maxStr
	lst = line.strip().split()

	# Get the length of maxStr (to be used for line checking)
	lengthMaxStr = len(maxStr.split())

	# line was split by whitespace and placed into lst
	# lst needs to contain at least 1 element for the DOLLARS amount plus
	#   the number of elements that rangeStr comprises
	# For example:
	# maxStr = "Up to", DOLLARS = "$1,000,000"
	# len(lst) should be at least 3 elements; 1 for DOLLARS + 2 for maxStr
	if len(lst) < lengthRangeStr + 1:
		return False	

	dollars = lst[2]
	dollars = getDollarAmount( dollars ) # get the integer value of DOLLARS
	# If dollars was not a dollar amount, return False
	lineMaxStr = lst[0].strip() + ' ' + lst[1].strip()
	# If maxStr cannot be found, return False
	if lineMaxStr.find(maxStr) == -1:
		return False

	return dollars


def dollarsRange ( line, splitter ):
	'''
	Returns the smaller DOLLARS amount in a "SMALLER_DOLLARS–LARGER_DOLLARS" line; False otherwise.
	NOTE: the hyphen between the dollar amounts is unicode character '\x96'. This character is used to
	split the dollar amounts from each other and is represented by the parameter splitter.
	This is passed in as a parameter in case future PDFs use a different character to split the amounts.
	'''

	# Split the line up by splitter to search for the two DOLLARS amounts
	lst = line.strip().split(splitter)

	# lst should be at least 2 elements due to the format of the line being checked for
	# SMALLER_DOLLARS, –, LARGER_DOLLARS where each DOLLARS should comprise of 1 element
	# NOTE: hypens are not recognized as a searchable element in uncf.txt for donation ranges
	# Example format:
	# lst = ["SMALLER_DOLLARS", "LARGERS_DOLLARS"]
	if len(lst) < 2:
		return False

	amount1 = lst[0]
	amount1 = getDollarAmount( amount1 ) # get the integer value of SMALLER_DOLLARS

	amount2 = lst[1]
	amount2 = getDollarAmount( amount2 ) # get the integer value of LARGER_DOLLARS

	# If amount1 or amount2 were not valid dollar amounts, return False
	if (not amount1) or (not amount2):
		return False

	# Return the integer represenation of SMALLER_DOLLARS
	return amount1


def getDollarAmount ( dollars ):
	'''Returns an interger representation of dollars; False otherwise.'''

	dollars = dollars.strip().split('$')
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
