import os
from flask import Flask, render_template, redirect, url_for, request, make_response
from flaskext.sqlalchemy import SQLAlchemy
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
        
@app.route("/", methods=['POST'])
def addURL():
    url = Url(request.form['url'])
    db.session.add(url)
    db.session.commit()
    return 'id: %(id)d' % { 'id': url.id }
    
@app.route("/<short_url>")
def redirectToId(short_url):
    url = Url.query.get(short_url)
    return redirect(url.url)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
