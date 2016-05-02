			Fully Featured Web Scraper
Further development of a more generalized web scraper, to be able to automate
the pulling of donor report PDFS, is the biggest hurdle to the scalability of this system.

Were this to be accomplished, the web scraper could automatically feed the PDFs into
the system, and the system could continuously scrape nonprofit websites in an exponential
fashion, until it has nearly scraped all of them and gathered their donor report data.



			Scraper Error Detection
A system for potential error detection and flagging would be necessary.
Potentially, the system could simply have a "staging" database, where large chunks of
PDFs for various nonprofits are committed to.
A user or administrator would then simply glance over the results of the staging parsing data,
and choose to commit to the production database, or choose to deny the results,
which would put them into a queue for problematic scrapes/parsers.



			Plug-and-play Web Template Interface
- To create a web page that allows a user to 
	1) upload (a) pdf(s) for a non profit not in the system
	2) specify some key parameters unique to the format
	   of each nonprofit's pdfs (phrase where data starts,
	   where data ends, etc.)
	3) press a button to run a generalized template now
	   customized with the provided parameters,
	   and produce its output live on the same page
	4) continue to make modifications to the generalized
       parameters until the user is satisfied that they
       meet the requirements, and can be used for a wide
       range of PDFs for that nonprofit
    5) press a button to commit this now customized template
       to the system, allowing new users to simply upload pdfs
       for that nonprofit

Ideally, within the same web page the user could see
	- the text of the uploaded pdf after being stripped of formatting to plaintext
	- the customizable parameters they're editing
	- the output of their customized template being run on the PDF(s) provided
all without having to refresh or leave that page.

This would reduce the barrier of entry so that less skilled labor forces could be used
to quickly customize, test, and produce working templates for large numbers of nonprofits.

If this could be accomplished, any user unskilled in programming or Python programming
could easily create a template for a new nonprofit, test it to prove its correctness,
and upload all pdfs for that nonrprofit within 5 minutes or so.
	Roughly 10 nonprofits x n PDFs per nonprofit per hour.
	With m donor records per PDF, this would result in 10*n*m donor records added to the system every hour for every user.
	With conservative estimates of n = 5, m = 100, this is 5000 donor records per hour per user at the very least case.





			Simplified handler.py Architecture
With such a web interface, nonprofits would no longer need their own folders and own template.py files.
Each nonprofit could simply be stored in a database, along with its customization parameters.
This way handler.py would simply be another file in app/.




			Changing auth_server into a Database
While a C++ authentication server was written for this project, it would be more ideal
and customary to simply utilize a database for user authentication.




			Platform independence
This, along with the changes above, would remove the Unix dependency of the system 
(since the sockets used in the auth server are all unix APIs),
and thus any platform that supports Python's Flask and MySQL (or any database technology),
would be able to run the system with the same functionality.




			Containerization
Furthermore, to prevent regression faults with the updates of system software,
flask versions, mysql versions, etc, it would be best to containerize this software
in a Docker container or similar environment.

Thus no matter what underlying architecutre it is running on, the container would
insure the same functionality so long as Docker (or whatever containerization software)
were supported.



			Better GUI & View Authorization
A more user-friendly and modern web interface so that the database could be
leveraged as a product for clients, as well as view authorization so that
certain clients only had rights to view certain parts of the database.
			


