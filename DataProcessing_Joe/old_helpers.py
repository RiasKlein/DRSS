#################################################################################
# 										#
# helpers.py							        	#
#										#
#	Contains functions to help with reading templates                	#
# 									   	#
#	Written by: Joseph Bieselin			Spring 2016	   	#
#									        #
#################################################################################




#################################################################################
# 										#
#        	helpers below originally written for template 1		        #
# 										#
#################################################################################

def dollarsAndUp ( line, RANGE_STR ):
    '''Returns the DOLLARS amount in a "DOLLARS and up" line; False otherwise'''
    list = line.strip().split()

    if len(list) < 3:
        return False
        
    dollars = list[0]
    dollars = getDollarAmount( dollars )
    if ((not dollars) or (not dollars.isdigit())):
    #if not dollars:
        return False
    
    and_up = list[1].strip() + ' ' + list[2].strip()
    
    if and_up.lower() != RANGE_STR:
        return False
    
    return dollars
        

def dollarsRange ( line ):
    '''Returns the smaller dollar amount in a "SMALLER_DOLLARS - LARGER_DOLLARS" line; False otherwise'''
    list = line.strip().split()
    
    if len(list) < 3:
        return False
        
    amount1 = list[0]
    amount1 = getDollarAmount( amount1 )
    
    amount2 = list[2]
    amount2 = getDollarAmount( amount2 )
    
    if ( ( (not amount1) or (not amount1.isdigit()) ) or  \
         ( (not amount2) or (not amount2.isdigit()) ) ):
         return False
         
    return amount1
         
                        
def getDollarAmount ( string ):
    '''Returns an integer represented as a string from a dollar amount; False otherwise'''
    string = string.split('$')
    if len(string) == 1:
        return False
    string = string[1]

    return string.replace(',', '')
               
                                             
def removeAsterisks ( line ):
    '''
    Returns the passed in string with '*' and ' ' removed starting from the right side.
    Once any character that isn't an asterisk or space is hit, removal stops.
    '''
    return line.rstrip('*' + ' ')
    
    
    
    