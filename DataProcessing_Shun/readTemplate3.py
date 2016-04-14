#################################################################################
#                                                                               #
# readTemplate3.py																#
#																				#
#	Contains the reading procedure for files that conform to template 3			#
#	The key is the word 'Supporters' 
#	This was especially made to handle reports from: National Public Radio      #	
# 																			   	#																		   #
#	Written by: Shunman Tse										Spring 2016	   	#
#																			   	#
#################################################################################

def mergeLines ( line, next_line ):
	result = line.rstrip ('\n')
	result += (" " + next_line)
	return result

def readTemplate3 ( rfile ):
	# Create an output file to place relevant information
	wfile = open ("out_template3.txt", 'w')

	# ignore_list contains keywords for unwanted lines 
	ignore_list = ["", "FISCAL", "Fiscal", "SUPPORTERS"]
	
	# merge_list contains keywords for merging
	merge_list = ["Anderson Cancer Center\n", "Directorate (DHS)\n", "Insurance Company\n", "Association\n", "Bureau\n", "Family Foundation\n", "Authority\n", "Technology\n", "Hewlett Foundation\n", "Langeloth Foundation\n", "T. MacArthur Foundation\n", "Medical Center\n"]
	
	while True:
		line = rfile.readline()		# read a line from the donor report
		if not line: break			# stop reading when we reach the end of the report	
			
		# Stop when we find starting location of donors
		if 'NPR SUPPORTERS' in line:
			# Now that we're at the start of their list of supporters, start reading!
			
			# NPR does not provide the actual amount donated by donors
			wfile.write (">>> Donation Amount: Unlisted\n")
			
			line = rfile.readline()
			cont = True
			
			while(cont):
				# Check for the ending condition
				if ("STATEMENT OF FINANCIAL POSITION" in line):
					wfile.close()
					return
				
				# Check whether the line contains any ignore words, if so, ignore the line
				keep_line = True
				for word in ignore_list:
					if word in line:
						keep_line = False
				
				# Get rid of blank lines, lines with a single letter, and lines with the number 20
				if (line == '\n') or (len(line) == 2) or line == "20\n":
					keep_line = False
					
				if (keep_line):
					# So, we want to keep the line? Let's check whether there is a need for merging.
					
					# Get the last word of the current line
					last_word = line.rsplit(None, 1)[-1]
					
					if (last_word == 'the') or (last_word[-1] == ","):
						donor_name = line.rstrip ('\n')
						donor_name += (" " + rfile.readline())
						wfile.write(donor_name)
					# Look into the future and see if there is a need to merge
					else:
						last_pos = rfile.tell()
						next_line = rfile.readline()
						first_word = next_line.split (' ', 1)[0]
						if next_line in merge_list:
							donor_name = mergeLines (line, next_line)
							wfile.write(donor_name)
						elif (first_word == 'of'):
							donor_name = mergeLines (line, next_line)
							wfile.write(donor_name)
						else:
							rfile.seek(last_pos)
							wfile.write(line)					
					
				last_pos = rfile.tell()		# note our donor report location
				line = rfile.readline()		# get the next line
				if not line: break			# if line has nothing, end
				
				
			
			