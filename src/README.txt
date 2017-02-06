This app takes you through a flow of screens, allowing you to login, filter what report you would like to see, view what you filtered off of, and then log back out.

I was not able to get my application to take in data and display it in a table, but I do have a very nice flow of screens, with the ability to filter reports by facility and date or just date.

I chose to comment out the pieces of code in which I attempted to pull in the data I needed, because it only seemed to break my application. I left it commented out to show my attempt, but wanted to turn in a working application.


Files:
app.py - Flask app to be run via mod_wsgi
config.py — config file
lost_conifg.json — json config file

templates/
	facility_inventory_report.html — a template for a report showing inventory at a specific facility and date based upon user specifications
	in_transit_report.html — a template for a report showing in transit on a specific date		based upon user specifications
	index.html — a template for the root path
	login.html — a template for a simple login screen
	logout.html — a template for a simple logout screen
	report_menu.html — a template for allowing user to choose specifications based upon what report they wish to see
