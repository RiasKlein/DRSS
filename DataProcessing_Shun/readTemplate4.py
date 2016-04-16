#################################################################################
#                                                                               #
# readTemplate4.py																#
#																				#
#	Contains the reading procedure for files that conform to template 4			#
#	Starting locations identified by: '$500,000+'								#
#	This was especially made to handle reports from: 							#
#		National Fish & Wildlife Foundation (2014/2015) 						#	
# 																			   	#																		   #
#	Written by: Shunman Tse										Spring 2016	   	#
#																			   	#
#################################################################################

# extractValue
#	Function takes the first element with a '$' symbol and returns the value
def extractValue ( line ):
	# NFWF (2014) uses the unicode character, '\xad' to split their categories
	list = line.split ('\xad')
	
	# If our line is unchanged (2015 case)
	if len(list) < 2:
		list = line.split (' ')
	
	# Get the first element with a '$' symbol and store in "value" variable
	for word in list:
		if '$' in word:
			value = word
			break
	
	value = value.strip ('$')			# Remove the '$' symbol
	value = value.replace (',', '')		# Remove the commas
	return value
	
# merge_lines
#	Function takes the current line and merges with the next line
#	The \n character is stripped off
#	The result is returned 
def mergeLines ( line, next_line ):
	result = line.rstrip ('\n')
	result += (" " + next_line)
	return result

# readTemplate4
def readTemplate4 ( rfile ):
	# Create an output file for donor names
	wfile = open ("out_template4.txt", 'w')
	
	# Ignore list containing keywords for unwanted lines
	ignore_list = ["restore wildlife", "2015", "46", "47", "Anonymous"]
	
	# Merge list containing keywords for merging
	merge_list = ["Family Foundation\n", "Insurance Company\n", "Owners Master Association, Inc.\n"]
	
	while True:
		line = rfile.readline()
		if not line: break
		
		# Stop when we find starting location of donors
		if ('$500,000+' in line):
			# Now that we're at the start of the list of donors, start reading!
			
			wfile.write (">>> Donation Amount: 500000\n")
			
			line = rfile.readline()
			cont = True
			
			while (cont):
				
				# Check for the ending condition
				if ("2 0 1 4 d o n o r s" in line) or ("A scarlet tanager sings in" in line):
					wfile.close()
					return
					
				# Check whether the line contains any ignore words, if so, ignore it
				keep_line = True
				for word in ignore_list:
					if word in line:
						keep_line = False
						
				# Get rid of blank lines
				if (line == '\n'):
					keep_line = False
					
				# Convert letters for Societe Generale (2015)
				if '\xe9' in line:
					line = line.replace ('\xe9', 'e')
										
				# Check whether the line contains a new category for donation amount
				if ('$' in line):
					# If the line is the start of a new category, we want to print that
					category_value = extractValue (line)
					wfile.write(">>> Donation Amount: " + category_value + "\n")
					keep_line = False
					
				if (keep_line):		
					# So, we want to keep the line? Let's check if there's need to merge
					
					# Get the last word of the current line
					last_word = line.rsplit(None, 1)[-1]
					
					if (last_word == 'the') or (last_word == 'of') or (last_word == 'for') or (last_word == 'and') or (last_word[-1] == ",") or (last_word[-1] == "/") or (len(last_word) == 2 and last_word[-1] == "."):
						donor_name = line.rstrip ('\n')
						donor_name += (" " + rfile.readline())
						wfile.write(donor_name)
					# Look into the future and see if there is a need to merge
					else:
						last_pos = rfile.tell()
						next_line = rfile.readline()
						next_line = next_line.strip(' ' )
						first_word = next_line.split (' ', 1)[0]
						if next_line in merge_list:
							donor_name = mergeLines (line, next_line)
							wfile.write(donor_name)
						elif (first_word == 'of') or (first_word == 'for') or (first_word == 'and'):
							donor_name = mergeLines (line, next_line)
							wfile.write(donor_name)
						else:
							rfile.seek(last_pos)
							wfile.write(line)	
				
				last_pos = rfile.tell()
				line = rfile.readline()
				if not line: break