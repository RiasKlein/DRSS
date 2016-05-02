Data Processing Component

> Issue: Different organizations label their donor lists differently
Solution: Have templates to handle various cases

> Issue: PDFs cannot be read directly as text due to formatting
Solution: Use the pdftotext utility to convert the pdfs before reading them
	Usage: pdftotext -raw (PDF's name) (output file's name)

### Templates (also referred to by T_CODE in process.py)

0:	National Geographic (2012 / 2013 / 2015)
	Keys: '$' and "AND ABOVE"
	
1: 	United Negro College Fund 
	
2: 	American National Red Cross (2015)
	Keys: '$' and 'or more' and 'annually'
	
3: 	National Public Radio (2014 / 2015)
	Keys: 'NPR Supporters' and '2015 Supporters'
	
4: 	National Fish & Wildlife Foundation (2014/2015)
	Key: '$500,000+' 
	

