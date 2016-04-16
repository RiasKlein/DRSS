#################################################################################
#                                                                               #
# readTemplate3.py																#
#																				#
#	Contains the reading procedure for files that conform to template 3			#
#	Starting locations identified by: 'NPR Supporters' and '2015 Supporters'	#
#	This was especially made to handle reports from: National Public Radio      #	
# 																			   	#																		   #
#	Written by: Shunman Tse										Spring 2016	   	#
#																			   	#
#################################################################################

# merge_lines
#	Function takes the current line and merges with the next line
#	The \n character is stripped off
#	The result is returned 
def mergeLines ( line, next_line ):
	result = line.rstrip ('\n')
	result += (" " + next_line)
	return result

# readTemplate3
#	Function locates donors based on starting location in report
#	Results are written to an output file
def readTemplate ( rfile_path , wfile_path):
	# Create an output file to place relevant information
	rfile = open(rfile_path, "r")
	wfile = open (wfile_path, 'w')

	# ignore_list contains keywords for unwanted lines 
	ignore_list = ["As of", "", "FISCAL", "Fiscal", "SUPPORTERS"]
	
	# merge_list contains keywords for merging
	merge_list = ["Memorial Museum\n", "College of Management\n", "Traubert\n", "Society Press\n", "Company\n", "Foundation Inc.\n", "Processes\n", "Charitable Trust\n", "Charitable Remainder Trust\n", "Perlman\n", "Sturt Haaga\n", "Gustafson\n", "Steinhauser\n", "Grasseschi\n", "Broadcasting\n", "Board of Standards\n", "Cartwright\n", "Hospital\n", "Association of America\n", "Foundation\n", "Service\n", "Entertainment\n", "Anderson Cancer Center\n", "Directorate (DHS)\n", "Insurance Company\n", "Association\n", "Bureau\n", "Family Foundation\n", "Authority\n", "Technology\n", "Hewlett Foundation\n", "Langeloth Foundation\n", "T. MacArthur Foundation\n", "Medical Center\n"]
	
	while True:
		line = rfile.readline()		# read a line from the donor report
		if not line: break			# stop reading when we reach the end of the report	
			
		# Stop when we find starting location of donors
		if 'NPR SUPPORTERS' in line or ("2015 Supporters" in line):
			# Now that we're at the start of their list of supporters, start reading!
			
			# NPR does not provide the actual amount donated by donors
			wfile.write (">>> Donation Amount: Unlisted\n")
			
			line = rfile.readline()
			cont = True
			
			while(cont):
				# Check for the ending condition
				if ("STATEMENT OF FINANCIAL POSITION" in line) or ("Statements Of" in line):
					wfile.close()
					return
				
				# Strip the bullet points off of the lines (Applies to 2015 NPR)
				line = line.strip("\xb7 ")
				
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
					
					if (last_word == 'the') or (last_word == 'of') or (last_word == 'for') or (last_word == 'and') or (last_word[-1] == ",") or (len(last_word) == 2 and last_word[-1] == "."):
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
						elif (first_word == 'of') or (first_word == 'for') or (first_word == 'and'):
							donor_name = mergeLines (line, next_line)
							wfile.write(donor_name)
						else:
							rfile.seek(last_pos)
							wfile.write(line)					
					
				last_pos = rfile.tell()		# note our donor report location
				line = rfile.readline()		# get the next line
				if not line: break			# if line has nothing, end
				
				
			
			