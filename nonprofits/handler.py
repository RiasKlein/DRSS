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
def insert_into_db(parsed_filename):
	return True

for given_pdf in target_files:
	converted_txt_file = given_pdf.split(".")[0] + ".txt"
	subprocess.Popen(["pdftotext", "-raw", given_pdf, converted_txt_file])
	
	# change to passing just a dir and an abs file path to process
	read_file = open(converted_txt_file, "r")
	template.readTemplate(read_file, nonprofit_dir)
	
	insert_into_db(nonprofit_dir + "/out_template.txt")
	# subprocess.Popen(["rm", given_pdf, converted_txt_file, nonprofit_dir + "/out_template.txt"])
	
