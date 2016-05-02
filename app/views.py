from app import app
import os # for system file paths, for uploading
import subprocess # popen()
from flask import Flask, flash, render_template
from flask import redirect, request, url_for, session, Response
from werkzeug import secure_filename
from database import *
from auth_server import *
from operator import itemgetter # for sorting results nicer

'''
View functions:
- /, /login 		-->		home page for any user not logged in
- /view_data		-->		home page for any user logged in
- /upload_pdfs		-->		page for user to upload new pdfs
- /change_password	-->		page for user to change their password
- /register 		-->		page for ADMIN only to register new users
- /logout			-->		page for user to log out

Helper functions:
- /inline_edit		-->		page for handling x-editable inline edits
'''



# Home page is login page, no publicly viewable pages available.
@app.route('/', methods=['GET','POST'])
@app.route('/login', methods=['GET','POST'])
def login():
	# if user already logged in, redirect appropriately
	if 'username' in session:
		return redirect('/view_data')

	# if post form submitted, handle authentication with C++ server
	if request.method=='POST':
		if request.form["username"] == "" or request.form["password"] == "":
			flash("You have left a field empty!")
			return redirect('/')
		username = request.form["username"]
		password = request.form["password"]
		credentials = username + "\t" + password
		response = auth_server("LOGIN", credentials)
		if response.strip() == "SUCCESS":
			session["username"] = username
			return redirect('/view_data')
		else:
			flash(response)
			return redirect('/')

	# if no form submitted, return page for simply GET
	return render_template("login.html")



# Home page for any logged in user, allows user to view data.
@app.route('/view_data', methods=['GET','POST'])
def view_data():
	# if user not logged in, redirect appropriately
	if 'username' not in session:
		return redirect('/')

	# get various GET parameters and show results accordingly
	nonprofit = request.args.get("nonprofit")
	if nonprofit != None:
		year = request.args.get("year")
		if year != None:
			amount = request.args.get("amount")
			if amount != None:
				donors = get_data(nonprofit, year, amount)
				return render_template("view_data.html", nonprofit = nonprofit, year = year, amount = amount, donors = donors, logged_in = session['username'])
			amounts = list(get_data(nonprofit, year))
			amounts.sort(key=lambda t: int_sort(t[0]), reverse=True)
			return render_template("view_data.html", nonprofit = nonprofit, year = year, amounts = amounts, logged_in = session['username'])
		years = get_data(nonprofit)
		return render_template("view_data.html", nonprofit = nonprofit, years = years, logged_in = session['username'])

	# if no GET parameters specified, return just list of nonprofits
	nonprofits = get_data()
	return render_template("view_data.html", nonprofits = nonprofits, logged_in = session['username'])

def int_sort(tuple):
	try:
		return int(tuple)
	except:
		return 0

# Allows user to upload new pdfs into the system.
# Any repeated entries will simply receive a duplicate primary key
# error in the background, and not cause any problems.
@app.route('/upload_pdfs', methods=['GET', 'POST'])
def upload_pdfs():
	# if not already logged in, redirect appropriately
	if 'username' not in session:
		return redirect('/')

	# uses OS calls to generate appropriate absolute path to nonprofit directories
	app_dir = os.path.abspath(__file__) # path to this file
	app_dir = os.path.join(app_dir, "../..") # this file's parent dir's parent (drss)
	app_dir = os.path.abspath(app_dir) # convert that into an abs path
	nonprofits_dir = os.path.join(app_dir, NON_PROFITS_FOLDER)

	# if POST form submitted, saves each uploaded file ina ppropriate directory
	if request.method == 'POST':
		# if no nonprofit specified, reprompt user
		if request.form.get('nonprofit', None) is None:
			nonprofits = os.walk(nonprofits_dir).next()[1]
			return render_template("upload.html", error="Please select a nonprofit for your pdfs to be associated with.", nonprofits=nonprofits, logged_in = session['username'])
		uploaded_files = request.files.getlist("file[]")
		variable_directory = os.path.join(nonprofits_dir, request.form["nonprofit_choice"])
		target_files = []
		for file in uploaded_files:
			if file and '.' in file and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS:
				filename = secure_filename(file.filename)
				target_filename = os.path.join(variable_directory, filename)
				file.save(target_filename)
				target_files.append(target_filename)

		# do not use glob("*.pdf") for target_files; destroys multi-user concurrency
		# launches handler.py with only uploaded file names as the arguments
		handler_path = os.path.join(nonprofits_dir, "handler.py")
		result = subprocess.Popen(["python", handler_path, request.form["nonprofit_choice"]] + target_files)
		return redirect('/')

	# if no form submitted, return page for simply GET with list of nonprofits to submit to
	nonprofits = os.walk(nonprofits_dir).next()[1]
	return render_template("upload.html", nonprofits=nonprofits, logged_in = session['username'])



# Allows user to change their password.
@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
	# if not already logged in, redirect appropriately
	if 'username' not in session:
		return redirect('/')

	# if form submitted, verify with C++ server and return its response
	if request.method=='POST':
		if request.form["new_password"] == "" or request.form["password"] == "":
			flash("You have left a field empty!")
			return redirect('/')
		username = session['username']
		password = request.form["password"]
		new_password = request.form["new_password"]
		credentials = username + "\t" + password
		response = auth_server("CHANGE PASSWORD", credentials, new_password)
		if response.strip() == "SUCCESS":
			return redirect('/view_data')
		else:
			flash(response)
			return redirect('/change_password')

	# if no form submitted, return page for simply GET
	return render_template("change_password.html", logged_in = session['username'])



# Allows admin user ONLY to register new accounts.
# (This is handled in the register.html file which verifies session["username"])
@app.route('/register', methods=['GET', 'POST'])
def register():
	# if not already logged in, redirect appropriately
	if 'username' not in session:
		return redirect('/')

	# if form submitted, verify with C++ server and return its response
	if request.method=='POST':
		if request.form["username"] == "" or request.form["password"] == "":
			flash("You have left a field empty!")
			return redirect('/')
		username = request.form["username"]
		password = request.form["password"]
		credentials = username + "\t" + password
		response = auth_server("REGISTER", credentials)
		if response.strip() == "SUCCESS":
			return redirect('/view_data')
		else:
			flash(response)
			return redirect('/')

	# if no form submitted, return page for simply GET
	return render_template("register.html", logged_in = session['username'])



# Clears the session and redirects user to home page (login page)
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')



# Gets form values from an inline edit and updates the database accordingly.
# database.py::update_db() could return a json error, which would be shown to the user
# Empty JSON "{}" returned if somehow this is called without a POST form.
@app.route('/inline_edit', methods=['GET', 'POST'])
def inline_edit():
	if request.method == 'POST':
		nonprofit = request.args.get("nonprofit")
		year = request.args.get("year")
		amount = request.args.get("amount")
		old_donor = request.args.get("old_donor")
		new_record = request.form["value"]
		return update_db(nonprofit, year, amount, old_donor, new_record)
	return "{}"
