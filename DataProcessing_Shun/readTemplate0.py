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

# readTemplate0 (filename)
#	Function locates donors based on identifiers: '$' and 'AND ABOVE'
def readTemplate0 ( rfile, wfile ):
	while True:
		line = rfile.readline()		# read a line from the donor report
		if not line: break			# stop reading when we reach the end of the report		
		
		# Stop when we find the specified identifiers '$' and 'AND ABOVE'
		if '$' in line and 'AND ABOVE' in line:
			# Now that we found a list of donors, let's start reading them in
			
			# donation_value contains the value of the donation 
			donation_value = convertCommaDollarValue (line)
			wfile.write ("Donation Amount: " + str(donation_value))
			
			line = rfile.readline()	# this is the first donor in category
			cont = True				# variable to keep loop going
			
			# Now let's start getting some donor names
			while (cont):		
				wfile.write(line)			# write donor name into output	
				last_pos = rfile.tell()		# note our donor report location
				line = rfile.readline()		# get the next line
				if not line: break			# if line has nothing, end
				
				if '$' in line and 'AND ABOVE' in line:
					rfile.seek(last_pos)
					cont = False
			
			
			
		
	