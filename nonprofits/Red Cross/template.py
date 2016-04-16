#################################################################################
#                                                                               #
# readTemplate2.py																#
#																				#
#	Contains the reading procedure for files that conform to template 2			#
#	Template 2 uses the keys of '$', 'or more', 'annually'						#
#	This was especially made to handle: American Red Cross 2015 report          #	
# 																			   	#																		   #
#	Written by: Shunman Tse										Spring 2016	   	#
#																			   	#
#################################################################################

# convertDollarRedCross
#	Function takes a string containing a monetary value in the Red Cross 
#	donor reports / annual reports and converts it into an int that the system
#	can use. This functions for Red Cross reports from 2013 ~ 2015
def convertDollarRedCross ( string ):
	# Red Cross has 2 numbering conventions: ex. $1 million vs $250,000	
	if '$5,000,000' in string:
		return 5000000
	if '$1 million' in string or '$1,000,000' in string:
		return 1000000
	elif '$500,000' in string:
		return 500000
	elif '$250,000' in string:
		return 250000	

# merge_lines
#	Function takes the current line and merges with the next line
#	The \n character is stripped off
#	The result is returned 
def mergeLines ( line, next_line ):
	result = line.rstrip ('\n')
	result += (" " + next_line)
	return result		

# readTemplate2 
#	Function locates donors based on specific identifiers 
#	Donors are currently written to an output file.
def readTemplate ( rfile_path , wfile_path):
	# Create an output file to place relevant information
	rfile = open(rfile_path, "r")
	wfile = open (wfile_path, 'w')

	# ignore_list contains keywords for unwanted lines
	ignore_list = ["Anonymous", "*As of", "THANKS TO OUR SUPPORTERS", "life-changing and", "", "NATIONAL CORPORATE & FOUNDATION SPONSORS", "Annual gifts from", "those who rely on our", "in times of need.", "Red Cross"]
	
	# merge_list contains lines to look out for that should be merged with the previous line
	merge_list = ["Foundation\n"]
	
	while True:
		line = rfile.readline() 
		if not line: break
		
		if '$' in line and ('or more' in line or 'Annually' in line):
			
			# First, we determine the dollar value of the donations
			donation_value = convertDollarRedCross (line)
			wfile.write (">>> Donation Amount: " + str(donation_value) + "\n")
			
			line = rfile.readline()
			cont = True
			
			while (cont):
				# Checking for the ending condition
				# After donors, Red Cross talks about their Sources of Financial Support
				if ("Sources of Financial Support" in line):
					wfile.close()
					return
				
				# Check for the ending of the final donor list
				if ("The American Red Cross wishes to thank our most generous supporters." in line):
					break
					
				# Check whether there are keywords in the line for skipping this line
				keep_line = True
				for word in ignore_list:
					if word in line:
						keep_line = False
				
				if (line == '\n'):
					keep_line = False
					
				# If we still have our line at this point, keep it
				if (keep_line):
					# So we want to keep the line, let's attempt to deal with some multi-line names
					
					# Look into the future (or the next line) and see if there is a need to merge lines
					last_pos = rfile.tell()
					next_line = rfile.readline()
					if next_line in merge_list:
						donor_name = mergeLines (line, next_line)
						wfile.write(donor_name)
					else:
						rfile.seek (last_pos)
						wfile.write(line)
					
				last_pos = rfile.tell()		# note our donor report location
				line = rfile.readline()		# get the next line
				if not line: break			# if line has nothing, end
				
				# if the next line is a new category, then we want to move back
				# so when the loop repeats, we get an updated donation_value
				if '$' in line and ('or more' in line or 'Annually' in line):
					rfile.seek(last_pos)
					cont = False
				
				