#!/usr/bin/python
import MySQLdb
import socket
from flask import Flask, flash, render_template, redirect, request, url_for, session

# Create the Flask object
app = Flask(__name__)

mysql_host = "localhost"
mysql_user = "php_acc"
mysql_passwd = "Password1"
mysql_db = "drss"
AUTH_SERVER = "localhost"
AUTH_PORT = 13370

# for convenience of demonstration, this is all on one page.
# in reality, for scalability want to keep the queries as specific and small as possible.
# should have a page containing all REPORTED YEARS, each year linking to a separate page
# where all AMOUNT RANGES would link to a separate page, containing all donors
# for that (amount range, year).
def get_donor_html(website):
	# connect to database
	db = MySQLdb.connect(mysql_host, mysql_user, mysql_passwd, mysql_db)

	# create cursors for nested iterative queries
	cur_years = db.cursor()
	cur_amounts = db.cursor()
	cur_donors = db.cursor()

	# get all reported years
	cur_years.execute("select distinct d.year_given from Donations d where d.nonprofit = %s", (website,))

	# form an html table organized the way we want it
	records = []
	for year in cur_years.fetchall():
		records.append("<table border='1'><tr><td><b><u>" + str(year[0]) + "</b></u></td></tr>")
		cur_amounts.execute("select distinct d.amt_range from Donations d where d.nonprofit = %s and d.year_given = %s", (website, year[0]))
		# for every reported year, get the amount ranges for donations
		for amount in cur_amounts.fetchall():
			records.append("<table border = '1'><tr><td><b>" + amount[0] + "</b></td></tr>")
			cur_donors.execute("select distinct d.donor from Donations d where d.nonprofit = %s and d.year_given = %s and d.amt_range = %s", (website, year[0], amount[0]))
			# for every amount range list all the donors
			for donor in cur_donors.fetchall():
				records.append("<tr><td>" + donor[0] + "</td></tr>")
			records.append("</table>")
		records.append("</table><br><br>")

	# close database, return html donor list	
	db.close()
	return records
 
def get_nonprofits():
	# connect to database
	db = MySQLdb.connect(mysql_host, mysql_user, mysql_passwd, mysql_db)

	# create cursors for nested iterative queries
	cur_nonprofits = db.cursor()

	# get all scraped nonprofits
	cur_nonprofits.execute("select distinct d.nonprofit from Donations d")

	# close database, return nonprofits list
	db.close()
	return cur_nonprofits.fetchall()

def valid_credentials(username, password):
	return auth_server("LOGIN", credentials)
	
# Returns response string, either success or error message
def auth_server(request_type, credentials, new_password=""):
	# connect to server, send request
	connfd = socket.socket()
	connfd.connect((AUTH_SERVER,AUTH_PORT)) 
	connfd.send(request_type + "\r\n")

	# get response, handle errors
	response = connfd.recv(1024)
	if response.strip() != "VALID REQUEST":
		connfd.close()
		return response
	# to login, verify credentials
	if request_type == "LOGIN" or request_type == "REGISTER":
		connfd.send(credentials + "\r\n")
		response = connfd.recv(1024)
		connfd.close()
		return response
	# to change password, first validate credentials
	elif request_type == "CHANGE PASSWORD":
		if new_password == "":
			connfd.close()
			return "Please enter in a new password."
		connfd.send(credentials + "\r\n")
		response = connfd.recv(1024)
		print "resp1" + response
		# if validated, change password
		if response.strip() != "SUCCESS":
			connfd.close()
			return response
		connfd.send(new_password + "\r\n")
		response = connfd.recv(1024)
		print "resp2" + response
		connfd.close()
		return response

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/', methods=['GET','POST'])
@app.route('/login', methods=['GET','POST'])
def login():
	if 'username' in session:
		return redirect('/index')
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
			return redirect('/index')
		else:
			flash(response)
			return redirect('/')
	return render_template("login.html")
 
@app.route('/index', methods=['GET','POST'])
def index():
	if 'username' not in session:
		return redirect('/')
	nonprofit = request.args.get("nonprofit")
	if nonprofit != None:
		records = get_donor_html(nonprofit)
		return render_template("index.html", records = records, nonprofit = nonprofit, logged_in = session['username'])
	nonprofits = get_nonprofits()
	return render_template("index.html", nonprofits = nonprofits, logged_in = session['username'])

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
			return redirect('/index')
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
			return redirect('/index')
		else:
			flash(response)
			return redirect('/change_password')
	return render_template("change_password.html", logged_in = session['username'])

app.secret_key = 'DRSS is pronounced duhhrs'
# Run the Flask application
app.run("localhost", 8000, debug = True)

