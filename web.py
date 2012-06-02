import os
import simplejson
from flask import Flask, render_template, redirect, url_for, request, make_response, abort
from flaskext.sqlalchemy import SQLAlchemy
from b64 import *
from url_validator import is_valid_url
from skip32 import skip32

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')

id_hider = skip32(os.environ.get('SECRET_KEY'))

if not os.environ.get('PROD'):
    app.config['SQLALCHEMY_ECHO'] = False
    app.debug = True

db = SQLAlchemy(app)

class Url(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url_address = db.Column(db.String)

    def __init__(self, url_address):
        self.url_address = self.validate_url_heuristically(url_address)
            
    def validate_url_heuristically(self, url_address):
        if not is_valid_url(url_address):
            url_address = 'http://' + url_address;
            if not is_valid_url(url_address):
                raise ValueError('Invalid URL')
        return url_address
        
    def short_url(self):
        return num_encode(id_hider.hide_id(self.id))
        
    @classmethod
    def id_for_short_url(cls, short_url):
        return id_hider.unhide_id(num_decode(short_url))

@app.route("/")
def index():
    return render_template('index.html')

REQUEST_URL_PARAMETER_NAME='url_address'

@app.route("/", methods=['POST'])
def add_url_route():
    url = new_url_from_address_handling_errors(request.form[REQUEST_URL_PARAMETER_NAME])
    url = craete_or_retrieve_url_from_db(url)
    return create_json_response_with_short_url(url.short_url())
    
def new_url_from_address_handling_errors(url_address):
    try:
        return Url(url_address)
    except ValueError:
        abort(400)

def craete_or_retrieve_url_from_db(url):
        existing_url = retrieve_url_with_url_address(url.url_address)
        if existing_url is not None:
            return existing_url
        return add_url_to_db(url)

def retrieve_url_with_url_address(url_address):
    return Url.query.filter_by(url_address=url_address).first()
            
def add_url_to_db(url):
    db.session.add(url)
    db.session.commit()
    return url;

def create_json_response_with_short_url(short_url):
    response = make_response()
    response.headers['Content-Type'] = 'application/json'
    response.data = simplejson.dumps({'short_url':short_url})
    return response;
    
@app.route("/<short_url>")
def redirect_route(short_url):
    id = id_for_short_url_handling_errors(short_url)
    url = Url.query.get(id) or abort(404)
    return redirect(url.url_address)
        
def id_for_short_url_handling_errors(short_url):
    try:
        return Url.id_for_short_url(short_url)
    except ValueError:
        abort(404)
         
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
