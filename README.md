Short Urls
==========

Yet an other url shortener. Because there isn't enough out there! This is a project build with Python using Flask and SQLAlchemy. The backend talks json which the front end consumes with jQuery. The DOM model of the page is updated with results from the queries without loading the whole page.

The project has lots of tests and serves as the documentation of the project.

A live instance of the app can be found at [s.emreberge.com](http://s.emreberge.com/)

Scaling
-------

To handle the increasing amount of requests the database can be copied regularly and used by several instances of the app that redirect short urls. So URLs are created by a single instance but lookups are made by several. But what happens if a lookup is made before that entry is copied to the helper instances? To prevent error this may cause, the helper instances should forward the lookup to the main instance incase it can't be found on the helper instances database.

Setup & Run
-----------

### Locally

Install postgres

	brew install postgres
	
Initialize db

    initdb /usr/local/var/postgres

Start postgres

    postgres -D /usr/local/var/postgres
	
Create a database (with shortUrls as database name)

    createdb shortUrls
  
If you get the following error:

    psql: could not connect to server: Permission denied
        Is the server running locally and accepting
        connections on Unix domain socket "/var/pgsql_socket/.s.PGSQL.5432"?

The fix is [here](http://nextmarvel.net/blog/2011/09/brew-install-postgresql-on-os-x-lion/)
	
Resolve requirements

    sudo pip install -r requirements.txt
			
Set the `DATABASE_URL` environment variable to point to your PostgreSQL server:

    export DATABASE_URL=postgres://<user_name>@localhost/ShortUrls
    
Set the `SECRET_KEY` environment variable. This is used to hide the internal id structure from the external one. **THIS HAS TO BE 10 CHAR LONG**

    export SECRET_KEY=secret-key
    
Create the tables

    python manage.py create_all

Run tests (tests are run with a in memory database)

    python test.py

Run the app

    python web.py
	
Checkout the website

    open http://localhost:5000

### Heroku
	
[Get Heroku](https://devcenter.heroku.com/articles/quickstart)

Create an app

    heroku create -s cedar

Add shared database add on

    heroku addons:add shared-database
    
Optionally add a custom domain (you have to also add a CNAME to your DNS settings to point to the heroku address of the app)

    heroku domains:add <custom domain>
    
Configure the secret key **THIS HAS TO BE 10 CHAR LONG**

    heroku config:add SECRET_KEY=secret-key

Optionally configure google analytics

    heroku config:add ANALYTICS_TRACKING_ID=<Your Tracking ID>

Deploy

    git push heroku master
  
Create the tables

    heroku run "python manage.py create_all"
  
Run the app

    heroku open
  
Switch to production mode

    heroku config:add PROD=True
  
API
---

### Create a short url

    curl -d "url_address=www.emreberge.com" <short-url-site>/

Response:
    
    {"short_url": "B"}

### Redirect for short url

    curl -I http://short-url.emreberge.com/B

Response:
    
    HTTP/1.1 302 FOUND
    Location: http://www.emreberge.com
