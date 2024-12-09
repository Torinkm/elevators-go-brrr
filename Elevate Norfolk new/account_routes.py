#   Imports   #

from flask import Flask, render_template, flash, redirect, url_for, request, session
from forms import NameForm, LoginForm
from db_connector import database
import hashlib
import datetime

from __main__ import app, db

#   Routes   #

@app.route('/login', methods = ['POST', 'GET'])
def login():
    form = LoginForm()
    current_user = session.get('user')

    #   If someone has already signed in redirect them to home page
    if current_user:
        flash('Already Logged in!', 'info')
        return redirect(url_for('home'))

    if request.method == 'POST':
        #   get the uhhhh uherrr email from the formd
        user = request.form['Username']
        password = request.form['Password']
        #   we ghash the pasword guys no way
        hashed_password = hashlib.md5(str(password).encode()).hexdigest()
        #   grab the data of a user
        found_user = db.queryDB("SELECT * FROM users WHERE Username = ?", [user])

        #   check password matches
        if found_user:
            stored_password = found_user[0][3]   #   Assuming password in column 4
            if stored_password == hashed_password:
                session['user'] = user
                session['email'] = found_user[0][2] # asuming emale in column 3
                if found_user[0][4] == 'TRUE':
                    session['admin'] = True
                else:
                    session['admin'] = False
                flash("Successfully Logged In!", "success")
                return redirect(url_for("home"))
            else:
                flash("Incorrect Password", "danger")
        else:
            flash("User not found", "danger")

    return render_template(
        'login.html',
        current_user = current_user,
        form = form
    )

@app.route('/logout')
def logout():
    flash('You have been Logged out!', 'danger')
    session.pop('user', None)
    session.pop('email', None)
    session.pop('admin', None)
    return redirect(url_for('home'))

@app.route('/register', methods = ['POST', 'GET'])
def register():
    current_user = session.get('user')

    #   If someone has already signed in redirect them to home page
    if current_user:
        flash('Already signed in.', 'info')
        return redirect(url_for('home'))

    if request.method == 'POST':
        user = request.form['Username']
        email = request.form['Email']
        password = request.form['Password']
        confirmPassword = request.form['ConfirmPassword']
        
        #   Check if the passwords match
        if password != confirmPassword:
            flash('Passwords do not match', 'danger')
            return redirect(url_for('register'))

        #   Validate the inputs
        if user == "" or email == "" or password == "":
            flash('Your not supposed to be here.', 'danger')
            return redirect(url_for('register'))
        
        #   Hash the password
        hashed_password = hashlib.md5(str(password).encode()).hexdigest()
        hashed_email = email#hashlib.md5(str(email).encode()).hexdigest()

        #   Check if the email or username is in use already
        result = db.queryDB("SELECT * FROM users WHERE Username = ? OR Email = ?", [user, hashed_email])
        if result:
            flash('Username or email already in use', 'danger')
            return redirect(url_for('register'))

        #   Anything here is accepted, update the database with user, email and password
        db.updateDB("INSERT INTO users(Username, Email, Password) VALUES (?,?,?)", [user, hashed_email, hashed_password])

        #   Set current session to newly created account
        session['user'] = user
        session['email'] = hashed_email
        session['admin'] = False

        #   Send them to home page
        return redirect(url_for('home'))
        
    else:
        return render_template(
            'register.html',
            current_user = session.get('user')
        )

@app.route('/adminregister', methods= ['POST', 'GET'])
def adminRegister():
    current_user = session.get('user')

    #   If someone has already signed in redirect them to home page
    if current_user:
        flash('Already signed in.', 'info')
        return redirect(url_for('home'))

    if request.method == 'POST':
        user = request.form['Username']
        email = request.form['Email']
        password = request.form['Password']
        confirmPassword = request.form['ConfirmPassword']
        
        #   Check if the passwords match
        if password != confirmPassword:
            flash('Passwords do not match', 'danger')
            return redirect(url_for('register'))

        #   Validate the inputs
        if user == "" or email == "" or password == "":
            flash('')
            return redirect(url_for('register'))
        
        #   Hash the password
        hashed_password = hashlib.md5(str(password).encode()).hexdigest()
        hashed_email = email#hashlib.md5(str(email).encode()).hexdigest()

        #   Check if the email or username is in use already
        result = db.queryDB("SELECT * FROM users WHERE Username = ? OR Email = ?", [user, hashed_email])
        if result:
            flash('Username or email already in use')
            return redirect(url_for('register'))

        #   Anything here is accepted, update the database with user, email and password
        db.updateDB('INSERT INTO users(Username, Email, Password, Admin) VALUES (?,?,?, "TRUE")', [user, hashed_email, hashed_password])

        #   Set current session to newly created account
        session['user'] = user
        session['email'] = hashed_email
        session['admin'] = True

        #   Send them to home page
        return redirect(url_for('home'))

    else:
        return render_template('adminRegister.html',
        current_user = current_user,
        admin = session.get('admin'))
