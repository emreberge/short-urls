import os
from flask import Flask, render_template, redirect, url_for, request, make_response
from flaskext.sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')

if not os.environ.get('PROD'):
    app.config['SQLALCHEMY_ECHO'] = True
    app.debug = True

db = SQLAlchemy(app)

class Urls(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String)

    def __init__(self, name):
        self.name = name


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
