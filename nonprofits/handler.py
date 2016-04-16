import sys
import os
import subprocess

ARG_FOLDER = 1
app_dir = os.path.dirname(__file__)
nonprofit_dir = os.path.join(app_dir, sys.argv[ARG_FOLDER])
sys.path.append(nonprofit_dir)
import template

# [python] handler.py <folder> <file_1> ... <file_N>
# [omitted] <variable>
target_files = sys.argv[(ARG_FOLDER+1):]

# dummy function for now
def insert_into_db(parsedFile_path):
	return True

for given_pdf in target_files:
	# filename.pdf -> filename.txt
	converted_txt_file = given_pdf.split(".")[0] + ".txt"
	# .call() not .Popen(), since need to wait for this to finish
	subprocess.call(["pdftotext", "-raw", given_pdf, converted_txt_file])

	split_path = os.path.split(converted_txt_file)
	parent_dir = split_path[0]
	file_name = split_path[1]
	# read filename.txt, write out_filename.txt
	read_file = os.path.join(parent_dir, file_name)
	write_file = os.path.join(parent_dir, "out_" + file_name)
	template.readTemplate(read_file, write_file)

	# insert out_filename.txt into database
	insert_into_db(write_file)

	# clean up filename.pdf, filename.txt, out_filename.txt
	subprocess.Popen(["rm", given_pdf, read_file, write_file])
	
