#################################################################################
# 																			   	#
# readTemplate0.py																#
#																				#
#	Contains the reading procedure for files that conform to template 0			#
#	Template 0 uses the '$' symbol and 'AND ABOVE' to locate donors				#
#	This was especially made to handle files from: National Geographic			#	
# 																			   	#																		   #
#	Written by: Shunman Tse										Spring 2016	   	#
#																			   	#
#################################################################################

# convertCommaDollarValue
#	Function takes a string containing a monetary value with '$' symbol and 
#	is comma separated and converts it into an int that the system can uses
#	That is: $1,000,000 will be converted to 1000000
def convertCommaDollarValue ( string ):
	value = -1							# default value
	value_string = ""
	array = string.split(" ")			# use whitespace as a delimiter 
	for word in array:					# iterate through the array
		if '$' in word:					# check if there is a '$' symbol
			word = word.strip ('$')		# remove the '$' symbol
			value_list = word.split(",")	# use ',' as a delimiter
			for i in value_list:		# create string form of number
				value_string += i
			value = int(value_string)	# convert number to int
			break
	return (value)						# return the int so it can be used
	
# merge_lines
#	Function takes the current line and merges with the next line
#	The \n character is stripped off
#	The result is returned 
def mergeLines ( line, next_line ):
	result = line.rstrip ('\n')
	result += (" " + next_line)
	return result

# readTemplate0 
#	Function locates donors based on identifiers: '$' and 'AND ABOVE'
#	Donors are currently written to an output file.
def readTemplate0 ( rfile ):
	# Create an output file to place relevant information
	wfile = open ("out_template0.txt", 'w')

	# ignore_list contains keywords for unwanted lines in 2012 ~ 2015 national geographic annual reports
	ignore_list = ["CLICK", "SUPPORT EXPLORATION", "NATIONAL GEOGRAPHIC", "National Geographic", "ACKNOWLEDGMENT OF GIFTS", "would be like had it", "to many people and made", "NORMA SHAW", "ANNUAL REPORT", "", "Anonymous", "organization creates a", "images and narratives", "cultures, their arts,", "THE POWER OF PHILANTHROPY", "can spark conversations", "important issues we face", "better care of each other", "Member", "our planet and all", "for our grandchildren", "world through scientific", "Together we are making", "and journalists. We", "of the generous individuals,", "and agencies shown here", "received between", "helped us inspire", "January 1 and December"]

	# merge_list contains keywords for entries that should be combined with the previous line
	merge_list = ["Foundation\n", "Foundation, Inc.\n", "LLC\n", "Fund, Inc.\n", "Family Foundation\n"]

	while True:
		line = rfile.readline()		# read a line from the donor report
		if not line: break			# stop reading when we reach the end of the report		
		
		# Stop when we find the specified identifiers '$' and 'AND ABOVE'
		if '$' in line and 'AND ABOVE' in line:
			# Now that we found a list of donors, let's start reading them in
			
			# donation_value contains the value of the donation 
			donation_value = convertCommaDollarValue (line)
			wfile.write (">>> Donation Amount: " + str(donation_value) + "\n")
			
			line = rfile.readline()	# this is the first donor in category
			cont = True				# variable to keep loop going
						
			# Now let's start getting some donor names
			while (cont):	
				# Checking for the ending condition in 3 different years of Nat-Geo files
				if ("Deceased" in line or "Bequest" in line):
					wfile.close()
					return
			
				keep_line = True
				for word in ignore_list:
					if word in line:
						keep_line = False
				
				if (line == '\n'):
					keep_line = False

				if (keep_line):
					# So we want to keep the line, let's attempt to deal with some double line entries
					
					# If the last word of our current entry is 'and' / 'for', then we definitely want to merge the next line
					last_word = line.rsplit(None, 1)[-1]
					if (last_word == 'and') or (last_word == 'for') or (last_word == 'of') or (last_word == 'at'):
						donor_name = line.rstrip ('\n')
						donor_name += (" " + rfile.readline())
						wfile.write(donor_name)
					# If the next line is one of the merge keywords such as 'Foundation', then we will merge
					else:
						last_pos = rfile.tell()  # keep our position
						next_line = rfile.readline()
						first_word = next_line.split (' ', 1)[0]
						if next_line in merge_list:
							donor_name = mergeLines (line, next_line)
							wfile.write(donor_name)
						elif (first_word == 'and') or (first_word == 'for') or (first_word == 'of'):
							donor_name = mergeLines (line, next_line)
							wfile.write(donor_name)
						else:
							rfile.seek(last_pos)
							wfile.write(line)
					
				last_pos = rfile.tell()		# note our donor report location
				line = rfile.readline()		# get the next line
				if not line: break			# if line has nothing, end
				
				# if the next line is a new category, then we want to move back
				# so when the loop repeats, we get an updated donation_value
				if '$' in line and 'AND ABOVE' in line:
					rfile.seek(last_pos)
					cont = False