		DOWNLOADING PACKAGE
# download mysql-apt-config<version>.deb from
# http://dev.mysql.com/downloads/repo/apt


		PRELIMINARY INSTALL
# install that repository, replacing <version> with the appropriate version number you downloaded
sudo dpkg -i mysql-apt-config<version>.deb 

# now choose the versions you want to install in the menus presented
sudo apt-get install mysql-server



		CLEARING DATABASE CREDENTIALS
# due to bugs installing on ubuntu, this clears the credentials

# /etc/mysql/my.cnf must have the following lines
 [client]
 port	    	= 3306
 socket		= /var/run/mysqld/mysqld.sock
 host		    = 127.0.0.1
# this file is often missing the host part

# stop the service
sudo service mysql stop

# launch it bypassing the credentials
sudo mysqld_safe --skip-grant-tables &

	# launch the terminal mysql client
	mysql -u root

	# set some password for root to allow you to access the system
	use mysql; # mysql's default database
	update user set password=PASSWORD("somepassword") where User='root';

	# commit those changes and quit the mysql client
	flush privileges;
	quit;

# restart the mysql service
sudo service mysql stop
sudo service mysql start

# log in using the credentials you specified
mysql -u root -p # prompt for password field


		ACTUAL INSTALLATION
# now just run the following command to install
# the GUI-friendly mysql workbench
sudo apt-get install mysql-workbench

