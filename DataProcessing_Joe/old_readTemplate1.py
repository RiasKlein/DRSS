#################################################################################
# 										#
# readTemplate1.py								#
#										#
#	Contains the reading procedure for files that conform to template 1	#
#	Template 1 uses the '$' symbol and 'and up' to locate donors		#
#	This was especially made to handle files from: UNCF                     #
# 									   	#
#	Written by: Joseph Bieselin			Spring 2016	   	#
#									        #
#################################################################################

from helpers import *

RANGE_STR = "and up"  # used for donation amounts, i.e. $1,000,000 and up
END_SEQ   = "an evening of stars"  # used to know when to stop reading donor data

#def readTemplate1( rfileName, amountsFileName, wfileName ):
#    try:
#        rfile = open(rfileName, 'r')
#    except IOError:
#        print "There was an IOError"
#        return
#    
#    try:
#        amountsFile = open(amountsFileName, 'w')
#    except IOError:
#        print "There was an IOError"
#        return
#        
#    findDonationAmounts( rfile, amountsFile )
#
#    rfile.close()
#    amountsFile.close()
#        
#    try:
#        rfile = open(rfileName, 'r')
#    except IOError:
#        print "There was an IOError"
#        return
#    try:
#        amountsFile = open(amountsFileName, 'r')
#    except IOError:
#        print "There was an IOError"
#        return
#    
#    try:
#        wfile = open(wfileName, 'w')
#    except IOError:
#        print "There was an IOError"
#        return
#        
#    getDonorNames( rfile, amountsFile, wfile )
#    
#    rfile.close()
#    amountsFile.close()
#    wfile.close()

def readTemplate1 ( rfileName, wfileName ):
    try:
        rfile = open(rfileName, 'r')
    except IOError:
        print "IOError - opening read file."
        return
    
    try:
        wfile = open(wfileName, 'w')
    except IOError:
        print "IOError - opening write file."
        return
    
    try:
        findDonationStart( rfile )
    except:
        print "Error in findDonationStart function."
    #finally:
    #    rfile.close()
    #    wfile.close()
    #    return
        
    try:
        processDonors( rfile, wfile )
    except:
        print "Error in processDonors function."
    finally:
        rfile.close()
        wfile.close()
        return

def findDonationStart ( rfile ):
    '''Places rfile's file pointer at the beginning of the line that contains
    the first donation amount information. For example, "$1,000,000 and up".'''
    
    while True:
        
        lastFilePosition = rfile.tell()
        
        line = rfile.readline().strip()	# read a line from the donor report
        
        # Stop reading and return False if no donation amounts were found
        if not line:
            return False
        
        # Reset the file pointer to the beginning of the line and end reading
        if dollarsAndUp( line, RANGE_STR ) or dollarsRange( line ):
            rfile.seek(lastFilePosition)
            return
    


def processDonors ( rfile, wfile ):
    '''Loops through rfile and writes to wfile.
    Information written corresponds to a donation amount followed by donors
    that donated said amount. All such amounts and donors in rfile are processed.'''
 
    line = rfile.readline().strip()   

    # Start processing the donation/donor data
    # Previously loop only breaks at end of file or when first donation amount is reached   
    while line:
        
        # End processing if the END SEQUENCE has been found
        if line.lower().find(END_SEQ) != -1:
            break
            
        # Get the data amount that will be stored in wfile to show how much the donation was
        elif dollarsAndUp( line ) or dollarsRange( line ):
            dollars = dollarsAndUp( line )
            if not dollars:
                dollars = dollarsRange( line )
            wfile.write(dollars + '\n')
        
        # If not the END, and not a donation amount, it is a donor name
        else:
            # Remove any possible asterisks at end of line and write the donor to the file
            wfile.write(removeAsterisks( line ) + '\n')
        
        # Read in the next line for further processing
        line = rfile.readline().strip()
    


#################################################################################
##                                                                              #
##                                                                              #
##                           HELPER FUNCTIONS                                   #
##                                                                              #
##                                                                              #
#################################################################################
#
#def dollarsAndUp ( line ):
#    '''Returns the DOLLARS amount in a "DOLLARS and up" line; False otherwise'''
#    list = line.strip().split()
#
#    if len(list) < 3:
#        return False
#        
#    dollars = list[0]
#    dollars = getDollarAmount( dollars )
#    if ((not dollars) or (not dollars.isdigit())):
#        return False
#    
#    and_up = list[1].strip() + ' ' + list[2].strip()
#    
#    if and_up.lower() != RANGE_STR:
#        return False
#    
#    return dollars
#        
#
#def dollarsRange ( line ):
#    '''Returns the smaller dollar amount in a "SMALLER_DOLLARS - LARGER_DOLLARS" line; False otherwise'''
#    list = line.strip().split()
#    
#    if len(list) < 3:
#        return False
#        
#    amount1 = list[0]
#    amount1 = getDollarAmount( amount1 )
#    
#    amount2 = list[2]
#    amount2 = getDollarAmount( amount2 )
#    
#    if ( ( (not amount1) or (not amount1.isdigit()) ) or  \
#         ( (not amount2) or (not amount2.isdigit()) ) ):
#         return False
#         
#    return amount1
#         
#                        
#def getDollarAmount ( string ):
#    '''Returns an integer represented as a string from a dollar amount; False otherwise'''
#    string = string.split('$')
#    if len(string) == 1:
#        return False
#    string = string[1]
#    string.replace(',', '')
#               
#                                             
#def removeAsterisks ( line ):
#    '''
#    Returns the passed in string with '*' and ' ' removed starting from the right side.
#    Once any character that isn't an asterisk or space is hit, removal stops.
#    '''
#    return line.rstrip('*' + ' ')
#    

