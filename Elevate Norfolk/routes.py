from __main__ import app

from flask import Flask,render_template,flash,redirect,url_for,session,request
# we need request, session, flash and redirect for our logins
#from forms import NameForm,LoginForm

#importing database will allow us access the databases from the db_connector file
from db_connector import database
# pip install requests and hashlib
import requests
import hashlib

#define db as database
db = database()

#this is how on the website you get from one page of the website to the other
@app.route('/')
def home():
    current_user = session.get('user')

    return render_template('home.html', current_user=current_user)

@app.route('/about')
def about():
    current_user = session.get('user')

    return render_template("about.html", current_user=current_user)

@app.route('/accessibility')
def accessibility():
    current_user = session.get('user')

    return render_template("accessibility.html", current_user=current_user)