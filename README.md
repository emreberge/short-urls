
Setup
-----

Local
-----

### Setup & Run

Install postgres
	brew install postgres
	
... Initialize postgres

Start postgres
	postgres -D /usr/local/var/postgres
	
Create a database
	...
	If you get the following error: "..." check this site ...
	<user_name>@localhost/<database_name>
	
Resolve requirements

	sudo pip install -r requirements.txt
		
Create the tables

	python manage.py create_all
	
Set the `DATABASE_URL` environment variable to point to your PostgreSQL server:

	export DATABASE_URL=postgres://<user_name>@localhost/<database_name>
	
Run the app 

	python web.py
	
Checkout the website

	open http://localhost:5000
	

Heroku
------
		
### Running


###

API
---

curl -d "url=www.emreberge.com" <short-url-site>/
	