# database credentials
mysql_host = "localhost"
mysql_user = "php_acc"
mysql_passwd = "Password1"
mysql_db = "drss"


import MySQLdb
import sys
import os
import subprocess

# Performs file path manipulation to determine the absolute path to
# the nonprofits folder that the pdfs have been uploaded to.
ARG_FOLDER = 1
app_dir = os.path.dirname(__file__)
nonprofit_dir = os.path.join(app_dir, sys.argv[ARG_FOLDER])
sys.path.append(nonprofit_dir)
import template

# [python] handler.py <folder> <file_1> ... <file_N>
# [omitted] <variable>
target_files = sys.argv[(ARG_FOLDER+1):]

# Inserts the parsed file output into the database line by line.
def insert_into_db(written_file, nonprofit, year_given):
	read_file = open(written_file, "r")
	donation_amt = 0
	# connect to database
	db = MySQLdb.connect(mysql_host, mysql_user, mysql_passwd, mysql_db)

	# create cursor to insert into database
	cur_insert = db.cursor()
	while True:
		line = read_file.readline().strip()	# read a line from the donor report
		if not line: break			# stop reading when we reach the end of the report	
		
		if line.split()[0] == ">>>":
			# >>>, Donation, Amount:, ###
			donation_amt = ' '.join(line.split()[3:])
		# insert every donor line appropriate
		else:
			try:
				cur_insert.execute("insert into Donations (donor, amt_range, nonprofit, year_given) values (%s, %s, %s, %s)", (line, donation_amt, nonprofit, year_given,))
				db.commit()
			except MySQLdb.IntegrityError as err:
				print err
			except :
			    print "Unexpected error:", sys.exc_info()[0]
	# close database, return nonprofits list
	db.close()

for given_pdf in target_files:
	# filename.pdf -> filename.txt
	converted_txt_file = given_pdf.split(".")[0] + ".txt"
	# .call() not .Popen(), since need to wait for this to finish
	subprocess.call(["pdftotext", "-raw", "-enc", "ASCII7", given_pdf, converted_txt_file])

	split_path = os.path.split(converted_txt_file)
	parent_dir = split_path[0]
	file_name = split_path[1]
	# read filename.txt, write out_filename.txt
	read_file = os.path.join(parent_dir, file_name)
	write_file = os.path.join(parent_dir, "out_" + file_name)
	template.readTemplate(read_file, write_file)

	# insert out_filename.txt into database
	year_given = file_name.split('_')[0] # YEAR_nonprofit.txt
	insert_into_db(write_file, sys.argv[ARG_FOLDER], year_given)

	# clean up filename.pdf, filename.txt, out_filename.txt
	# subprocess.Popen(["rm", given_pdf, read_file, write_file])
	
