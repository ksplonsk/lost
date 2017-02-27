This app takes you through a flow of screens, allowing you to login, or create a username and password. From either page you are then directed to a dashboard page, in which your current username is displayed.

Files:
app.py - Flask app to be run via mod_wsgi
config.py — config file
lost_conifg.json — json config file

templates/
	login.html- allows you to login with a previously created username and password
	create_user.html- allows you to create a username and set a password
	dashboard.html- shows you the currently logged in user
	unmatched.html- this page shows when a login is failed (either that user does not exist or password did not match)
	user_already_exists.html- this page shows when you attempt to create a user and that username already exists
	user_created.html- page shows when a user is successfully created
	add_asset.html- allows you to add an asset
	add_facility.html- allows you to add a facility
	asset_already_exists.html- page shown when you attempt to add an asset that already exists
	asset_dispose_error.html- page shown when you aren unable to dispose of an asset
	asset_report.html- page that allows you to select a facility and a date to see a report based on your specifications
	dispose_asset.html- page that allows you to select an asset to dispose of
	facility_already_exists.html- page that shows when you try to add a facility that already exists
