1) Getting Started

1a) Install following dependencies if not already met
pip: (Python Installer)
	sudo apt-get -y install python-pip

Flask: (Front End)
	sudo pip install Flask

MySQL for Python:
	apt-get install python-dev libmysqlclient-dev
	pip install MySQL-python

1b) Adjust the database credentials at the top of app.py
to any credentials with sufficient privilege on your mysql setup.
- Alternatively, create a new user with the credentials already present
in app.py.

1c) Run the sql file to generate the table and insert sample data.

1d) cd to the app/ directory, and run the Flask app
	python app.py

1e) Open a browser window and navigate to "localhost:8000"


