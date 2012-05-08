import os
from flask import Flask, render_template, redirect, url_for, request, make_response
from flaskext.sqlalchemy import SQLAlchemy
from b64 import *

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
        self.url = url
        
    def redirect(self):
        return redirect(self._unlocal_url());
        
    def _unlocal_url(self):
        http = 'http://'
        return self.url if self.url.startswith(http) else http + self.url
        
    def short_url(self):
        return num_encode(self.id)
        
    @classmethod
    def id_for_short_url(cls, short_url):
        return num_decode(short_url)
    
        
@app.route("/", methods=['POST'])
def add_url_route():
    id = add_url_to_db(request.form['url'])
    return 'id: %(id)d' % { 'id': id }
    
def add_url_to_db(url_string):
    url = Url(url_string)
    db.session.add(url)
    db.session.commit()
    return url.id
    
    
@app.route("/<short_url>")
def redirect_route(short_url):
    url = Url.query.get(short_url)
    return url.redirect()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
