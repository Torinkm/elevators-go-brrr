from flask import Flask, render_template, flash, redirect, url_for, request, session
from forms import NameForm, LoginForm
from db_connector import database
import hashlib

app = Flask(__name__)   #   Sets up the flask application
app.secret_key = 'int(burger)'

db = database()

@app.route('/')         #   Sets route for the file
def home():
    current_user = session.get('user')
    if app.debug == True: print(f'Loading Homepage as {current_user}')
    return render_template(
        'index.html',
        current_user = current_user,
        footer = True,
        admin = session.get('admin')
    )

@app.route('/about')
def about():
    return render_template(
        'about.html',
        current_user = session.get('user'),
        footer = True,
        admin = session.get('admin')
    )

#   Import routes   #
import session_routes, account_routes, user_page_routes, advice_routes

if __name__ == '__main__':
    app.run(debug=True)     #   opens developer side in debug mode