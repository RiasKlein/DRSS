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

# readTemplate0 (filename)
#	Function locates donors based on identifiers: '$' and 'AND ABOVE'
def readTemplate0 ( rfile, wfile ):
	while True:
		line = rfile.readline()		# read a line from the donor report
		if not line: break			# stop reading when we reach the end of the report
		line.rstrip ('\n')			# take out new line characters from the line
		
		# Stop when we find the specified identifiers '$' and 'AND ABOVE'
		if '$' in line and 'AND ABOVE' in line:
			# Now that we found a list of donors, let's start reading them in
			wfile.write (line)		# Right now we are simply outputting the categories