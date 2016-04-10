################################################################################
# 																			   #
# findDollar.py																   #
# 																			   #																		   #
#	Written by: Shunman Tse										Spring 2016	   #
################################################################################

# findDollar (filename)
#	Function will open the provided filename, read through the file and write 
#	each line that contains the '$' symbol into an output file. 
#		It is useful for visual inspection of the mentions of '$' in a file
def findDollar ( filename ):
	# Attempt to open the specified file
	# Print an error if there is one
	try:
		rfile = open (filename, 'r')	
	except:
		print "Error (findDollar): Failed to open the specified file. Make sure that the file is in the current directory."
		exit()
	
	# Since we have a valid file, open a output file for writing
	wfile = open ("out_findDollar.txt", 'w')
	
	while True:
		line = rfile.readline()		# read in a line from the donor report
		if not line: break			# make sure that we are not at the EOF
		line.rstrip ('\n')			# remove newline characters in the line that was read in
		if '$' in line and "AND ABOVE" in line:				
			wfile.write(line)		# if so, write the line into the output file
		
	# Close the files
	rfile.close()
	wfile.close()
	
	