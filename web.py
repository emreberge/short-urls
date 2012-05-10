import os
from flask import Flask, render_template, redirect, url_for, request, make_response, abort
from flaskext.sqlalchemy import SQLAlchemy
from b64 import *
from url_validator import is_valid_url

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')

if not os.environ.get('PROD'):
    app.config['SQLALCHEMY_ECHO'] = True
    app.debug = True

db = SQLAlchemy(app)

class Url(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String)

    def __init__(self, url):
        if is_valid_url(url):
            self.url = url
        elif is_valid_url('http://' + url):
            self.url = 'http://' + url
        else:
            raise ValueError('Invalid URL')
        
    def short_url(self):
        return num_encode(self.id)
        
    @classmethod
    def id_for_short_url(cls, short_url):
        return num_decode(short_url)
        
@app.route("/", methods=['POST'])
def add_url_route():
    short_url = add_url_to_db(request.form['url'])
    return short_url;
    
def add_url_to_db(url_string):
    try:
        url = Url(url_string)
        db.session.add(url)
        db.session.commit()
        return url.short_url()
    except ValueError:
        abort(400)
    
@app.route("/<short_url>")
def redirect_route(short_url):
    try:
        url = Url.query.get(Url.id_for_short_url(short_url)) or abort(404)
        return redirect(url.url)
    except ValueError:
        abort(404)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
