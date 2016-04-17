from app import app
import os # for system file paths, for uploading
import subprocess # popen()
from flask import Flask, flash, render_template
from flask import redirect, request, url_for, session, Response
from werkzeug import secure_filename
from database import *
from auth_server import *

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

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/', methods=['GET','POST'])
@app.route('/login', methods=['GET','POST'])
def login():
	if 'username' in session:
		return redirect('/view_data')
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
	return render_template("login.html")

@app.route('/view_data', methods=['GET','POST'])
def view_data():
	if 'username' not in session:
		return redirect('/')
	nonprofit = request.args.get("nonprofit")
	if nonprofit != None:
		year = request.args.get("year")
		if year != None:
			amount = request.args.get("amount")
			if amount != None:
				donors = get_data(nonprofit, year, amount)
				return render_template("view_data.html", nonprofit = nonprofit, year = year, amount = amount, donors = donors, logged_in = session['username'])
			amounts = get_data(nonprofit, year)
			return render_template("view_data.html", nonprofit = nonprofit, year = year, amounts = amounts, logged_in = session['username'])
		years = get_data(nonprofit)
		return render_template("view_data.html", nonprofit = nonprofit, years = years, logged_in = session['username'])
	nonprofits = get_data()
	return render_template("view_data.html", nonprofits = nonprofits, logged_in = session['username'])

@app.route('/register', methods=['GET', 'POST'])
def register():
	if 'username' not in session:
		return redirect('/')
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
	return render_template("register.html", logged_in = session['username'])

@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
	if 'username' not in session:
		return redirect('/')
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
	return render_template("change_password.html", logged_in = session['username'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/upload_pdfs', methods=['GET', 'POST'])
def upload_pdfs():
	if 'username' not in session:
		return redirect('/')
	app_dir = os.path.abspath(__file__) # path to this file
	app_dir = os.path.join(app_dir, "../..") # this file's parent dir's parent (drss)
	app_dir = os.path.abspath(app_dir) # convert that into an abs path
	nonprofits_dir = os.path.join(app_dir, NON_PROFITS_FOLDER)
	if request.method == 'POST':
		uploaded_files = request.files.getlist("file[]")
		variable_directory = os.path.join(nonprofits_dir, request.form["nonprofit_choice"])
		target_files = []
		for file in uploaded_files:
			if file and allowed_file(file.filename):
				filename = secure_filename(file.filename)
				target_filename = os.path.join(variable_directory, filename)
				file.save(target_filename)
				target_files.append(target_filename)
		# do not use glob("*.pdf") for target_files; destroys multi-user concurrency
		handler_path = os.path.join(nonprofits_dir, "handler.py")
		result = subprocess.Popen(["python", handler_path, request.form["nonprofit_choice"]] + target_files)
		return redirect('/')
	nonprofits = os.walk(nonprofits_dir).next()[1]
	return render_template("upload.html", nonprofits=nonprofits)