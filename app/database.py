import sys # for try-except
import MySQLdb
from flask import Response

mysql_host = "localhost"
mysql_user = "php_acc"
mysql_passwd = "Password1"
mysql_db = "drss"

def get_data(nonprofit="", year="", amount=""):
	# connect to database
	db = MySQLdb.connect(mysql_host, mysql_user, mysql_passwd, mysql_db)

	# create cursors for nested iterative queries
	cur = db.cursor()

	#execute appropriate action
	if nonprofit == "":
		cur.execute("select distinct d.nonprofit from Donations d order by d.nonprofit asc")
	elif year == "":
		cur.execute("select distinct d.year_given from Donations d where d.nonprofit = %s order by d.year_given desc", (nonprofit,))
	elif amount == "":
		cur.execute("select distinct d.amt_range from Donations d where d.nonprofit = %s and d.year_given = %s order by d.amt_range desc", (nonprofit, year))
	else:
		cur.execute("select distinct d.donor from Donations d where d.nonprofit = %s and d.year_given = %s and d.amt_range = %s order by d.donor asc", (nonprofit, year, amount,))

	# close database, return list
	db.close()
	return cur.fetchall()

def update_db(nonprofit, year, amt, donor, new_donor):
	# connect to database
	db = MySQLdb.connect(mysql_host, mysql_user, mysql_passwd, mysql_db)

	# create cursor for query
	cur = db.cursor()

	# delete old record, insert new. an empty field will just delete old
	try:
		cur.execute("delete from Donations where nonprofit = %s and amt_range = %s and year_given =%s and donor = %s", (nonprofit, amt, year, donor,))
		if new_donor != "":
			cur.execute("insert into Donations (donor, amt_range, nonprofit, year_given) values (%s, %s, %s, %s)", (new_donor, amt, nonprofit, year,))
	# on error, send back the message to be used for a pop up
	except :
		db.close()
		exc_type, exc_value, exc_traceback = sys.exc_info()
		resp = Response(response=str(exc_value[1]), status=500, mimetype="application/json")
		return resp

	# if success, commit changes
	db.commit()

	# close database, return success JSON
	db.close()
	return "{}"
	# return Response(status=200, mimetype="application/json")

