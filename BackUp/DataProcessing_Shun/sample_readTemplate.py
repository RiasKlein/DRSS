#################################################################################
#                                                                               #
# readTemplate.py																#
#																				#
#	Contains the newest template version for parsing nonprofit PDFS				#
#	It has been tailored to work with NFWF's reports from 2014 ~ 2015			#
#	To function with other nonprofits, changes are required.					#
#																			   	#																		   #
#	Written by: Shunman Tse										Spring 2016	   	#
#																			   	#
#################################################################################

# Global Lists 
#>>> The following lines have to be changed to fit the document that you are working with <<<

# Ignore list containing keywords for unwanted lines
ignore_list = ["restore wildlife", "2015", "46", "47", "Anonymous"]
	
# List of specific lines that are merged with the previous upon detection
merge_list = ["Family Foundation\n", "Insurance Company\n", "Owners Master Association, Inc.\n"]

# List of keywords to look for in the start and end of lines that would signify merging
se_merge_list = ['of', 'the', 'for', 'and']

# readTemplate
#	Function contains the code to read through the text version of the nonprofit PDFs
def readTemplate ( rfile ):
	# Create an output file for donor names
	wfile = open ("out_template.txt", 'w')
		
	# From this point, the nonprofit report will be parsed (read through) one line at a time
	while True:
		line = rfile.readline()		# Get a new line from the input document
		if not line: break			# If we've reached the end of the document, stop the program
		
		# Find the starting point of the list of donors in the document
# >>> The following lines have to be changed to fit the document that you are working with <<<
		if ('$500,000+' in line):
			# Now that we're at the start of the list of donors, start reading!
			wfile.write (">>> Donation Amount: 500000\n")
			
			line = rfile.readline()
			cont = True
			
			while (cont):
				# Check for the ending condition
# >>> The following line has to be changed to fit the document that you are working with <<<
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
# >>> The following line contains the function to extract dollar amount from something of the form $500,000+
					category_value = extractValue (line)
					wfile.write(">>> Donation Amount: " + category_value + "\n")
					keep_line = False
					
				if (keep_line):		
					# So, we want to keep the line? Let's check if there's need to merge
					
					# Get the last word of the current line
					last_word = line.rsplit(None, 1)[-1]
					
					if (last_word in se_merge_list) or (last_word[-1] == ",") or (last_word[-1] == "/") or (len(last_word) == 2 and last_word[-1] == "."):
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
						elif (first_word in se_merge_list):
							donor_name = mergeLines (line, next_line)
							wfile.write(donor_name)
						else:
							rfile.seek(last_pos)
							wfile.write(line)	
				
				last_pos = rfile.tell()
				line = rfile.readline()
				if not line: break
				
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