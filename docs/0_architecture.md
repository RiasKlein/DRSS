		FRONT-END OVERVIEW
The front-end web server (written in Python's Flask, residing in the "app/" folder) offers the following web pages:
- /, /login 		-->		home page for any user not logged in
- /view_data		-->		home page for any user logged in
- /upload_pdfs		-->		page for user to upload new pdfs
- /change_password	-->		page for user to change their password
- /register 		-->		page for ADMIN only to register new users
- /logout			-->		page for user to log out

		FRONT-END SPECIFICS
- /, /login
	This web page takes in user credentials and verifies them by communicating
	with the authentication server (auth_server) written in C++.
- /view_data
	This web page allows a logged in user to peruse through the contents of the database.
	Users are shown the following data as links:
		all nonprofits in the database				--> 	clicking on a link leads to
		all years scraped for a given nonprofit 	--> 	clicking on a link leads to
		all amounts scraped for a given year 		--> 	clicking on a link leads to
		all donors scraped for a given amount 		
	At the donor level of records, the user can click on any given record and perform
	in line modifications, which will be updated in the database (including just deleting that record).
	Any errors returned by the database will be shown to the user, preventing their edit, in JavaScript.
- /upload_pdfs
	This web page allows a logged in user to upload any number of new pdfs into the database,
	specifying which nonprofit the pdfs are associated with. 
	Note: that for now the PDFs must be preceded with the year they pertain to, eg "2015_<...>.pdf"
	On success, the user is redirected to the /view_data home page, 
	otherwise they are given the appropriate error message.
- /change_password
	This web page allows a logged in user to change their password, which is done by
	communicating with the authentication server written in C++.
- /register
	This web page allows only the username named "admin" to register new accounts 
	for new users. A link to this page will not be visible to any logged in user
	who is not "admin".
- /logout
	This web page simply logs the user out and redirects to the /, /login web page.








		BACK-END OVERVIEW
The other folders in the project are for the back-end, as follows:
- app/				--> 		all files for the Flask front-end are here
- auth_server/		-->			all files for the C++ authentication server are here
- docs/				-->			all high-level supplementary documentation is here
- mysql/			-->			all database schema files are here
- nonprofits/		-->			all information about nonprofits in the system and how to handle them


		BACK-END SPECIFICS
- app/
	This folder contains all the necessary code for the Python Flask front-end. 
	This includes:
		views.py, 		the pages viewable to any given user
		database.py, 	the functionality for communicating with the database
		auth_server.py,	the functionality for communicating with the auth_server

- auth_server/
	This folder contains all the code for the C++ authentication server,
	as well as the necessary Makefile to compile on the target platform 
	(Ubuntu 14.04).

	The server communicates with the Python Flask front-end by using sockets,
	and passing messages in a preshared protocol/API used on both Flask and the C++ server.

- docs/
	This folder contains all the relevant documentation for a high-level understanding and usage of the project.
	This is to supplement the individual README files for each individual folder, as well as the inline 
	commenting and documentation within the actual code.

- mysql/
	This simply contains an SQL script file that defines the simple structure
	for the single table in the database: (Donor, Amount, Nonprofit, Year).

	The rest of the backend interacts with the mysql database presuming that the table schema 
	is what is defined in that script file. If any changes are made to the naming of the script file,
	the Python backend will need to be updated accordingly.

- nonprofits/
	This folder contains two things:
		handler.py,			the python script that processes uploaded files into the database
		nonprofit folders,	a separate folder for each nonprofit in the system
	
	nonprofit folders
		Each nonprofit that is added to the system must have its own folder.
		The name of this folder will be the name of the nonprofit in the database.
		Thus naming a folder "UNCF" means all PDFs associated with that tag will be under the "UNCF" nonprofit in the database.
		Naming a folder "United Negro College Fund" means all PDFS associated with that tag will come up under that separate name in the database.

	template.py
		In addition to each nonprofit having its own folder, each of these folders must contain a file named "template.py".	
		This file is the python script that will be imported and used to scrape PDFs for that specific nonprofit.
		The requirements for function and file input/output requirements for a template.py file to be compatible with 
		handler.py are documented in the "adding_templates.md" documentation.


		Database Credentials:
- These are stored in two separate locations:
	app/config.py,				for the Flask application to use
	nonprofits/handler.py,		for the file upload handler to use