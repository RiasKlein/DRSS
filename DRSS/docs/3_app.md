1) Getting Started

1a) Install following dependencies if not already met
pip: (Python Installer)
	sudo apt-get -y install python-pip

Flask: (Front End)
	sudo pip install Flask

MySQL for Python:
	sudo apt-get install python-dev libmysqlclient-dev
	pip install MySQL-python

MySQL for Ubuntu:
	See detailed instructions in:
		ubuntu_mysql.md

1b) Adjust the database credentials in the app/config.py file
to any credentials with sufficient privilege on your mysql setup.
- Alternatively, create a new user with the credentials already present
in app.py.

1c) Run the sql script file to generate the table.

1d) cd to the app/ directory, and launch the system  (both the Flask app and the auth_server) by typing:
	python run.py

1e) Open a browser window and navigate to "localhost:5000" to view the website

