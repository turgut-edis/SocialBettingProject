from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE__URI'] = 'mysql+pymysql://root:password123@localhost/our_users'

@app.route('/')

def index():
    return "<h1>Hello World!</h1>"

@app.route('/user/<name>')

def user(name):
    return "<h1>Hello {}</h1>".format(name)
