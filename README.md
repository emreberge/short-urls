Short Urls
==========

Yet an other url shortener. Because there isn't enough out there! This is a project build with Python using Flask and SQLAlchemy. The backend talks json which the front end consumes with jQuery. The DOM model of the page is updated with results from the queries without loading the whole page.

The project has lots of tests and serves as the documentation of the project.

Scaling
-------

To handle the increasing amount of requests the database should be copied regularly and used by several instances of the app that redirect short urls.

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
		
Create the tables

    python manage.py create_all
	
Set the `DATABASE_URL` environment variable to point to your PostgreSQL server:

    export DATABASE_URL=postgres://<user_name>@localhost/ShortUrls

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
    
Pseudo encrypting the ids for hiding the id sequence from users
---------------------------------------------------------------

Inspired from [this](http://wiki.postgresql.org/wiki/Pseudo_encrypt) and [this](http://www.webthatworks.it/d1/content/pseudo-random-sequences-postgresql)

How ever, without modification, this will restrict the short urls to 32 bits.

Install the function:

    CREATE OR REPLACE FUNCTION pseudo_encrypt(VALUE int) returns bigint AS $$
    DECLARE
    l1 int;
    l2 int;
    r1 int;
    r2 int;
    i int:=0;
    BEGIN
     l1:= (VALUE >> 16) & 65535;
     r1:= VALUE & 65535;
     WHILE i < 3 LOOP
       l2 := r1;
       r2 := l1 # ((((1366.0 * r1 + 150889) % 714025) / 714025.0) * 32767)::int;
       l1 := l2;
       r1 := r2;
       i := i + 1;
     END LOOP;
     RETURN ((l1::bigint << 16) + r1);
    END;
    $$ LANGUAGE plpgsql strict immutable;

Setup the sequence and column default:

    create sequence short_url_seq owned by url.id;
    alter table pr
      alter column code
        set default
        pseudo_encrypt(nextval('short_url_seq'::int4));

Reseting the sequence

    select setval('short_url_seq', 1, true);
