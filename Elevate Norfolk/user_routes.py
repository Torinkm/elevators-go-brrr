from __main__ import app

from flask import render_template,flash,redirect,url_for,session, request 
# we need request, session, flash and redirect for our logins
from forms import NameForm,LoginForm

#importing database will allow us access the databases from the db_connector file
from db_connector import database
# pip install requests and hashlib
import requests
import hashlib

#define db as database
db = database()

@app.route('/login', methods = ["POST", "GET"])
def login():
    title = "LOG IN"
    form = LoginForm()
    if request.method == "POST":
        # get the email from the form name=email 
        user = request.form ["email"]
        # get the password from the form
        password = request.form ['password']

        # we hash the inputted password
        hashed_password = hashlib.md5(str(password).encode()).hexdigest()
        # check if a user exists
        found_user = db.queryDB("SELECT * FROM user WHERE username = ?",[user])

        # check the password matches the username
        if found_user:
            stored_password = found_user [0][3] # assuming password is in 3th column
            if stored_password == hashed_password:
                session['user'] = user
                session['email'] = found_user [0][1]
                flash("login successful", 'success')
                return redirect(url_for("home"))
            else:
                flash("Incorrect Password","danger")
        else:
            flash("user not found","danger")

    if "user" in session:
        flash("Already Logged In !", "info")
        return redirect(url_for("user"))
    else:
        return render_template('login.html', form=form)

    return render_template('login.html',title=title, form=form)


@app.route("/user")
def user():
    title = "User Page"
    current_user = session.get('user')
    return render_template('user.html',title=title, current_user=current_user)

@app.route("/register", methods=['GET', 'POST'])
def register():
    title = "Registration Page"
    current_user=session.get('user')
    if request.method == "POST":
        user = request.form["nm"]
        password = request.form["pword"]
        email = request.form["email"]

        # hash email and password
        hashed_password = hashlib.md5(str(password).encode()).hexdigest()
        hashed_email = hashlib.md5(str(email).encode()).hexdigest()
        result = db.queryDB("SELECT * FROM user WHERE username = ? OR email = ?", [user,hashed_email])
        if result:
            flash('Email or User Name already Exists, please try a different one', "danger")
            return redirect(url_for('register'))
        # update the DB with user, hashed email and Password
        db.updateDB("INSERT INTO user (username, email, password) VALUES (?,?,?)", [user,hashed_email,hashed_password])
        return render_template('login.html', title = 'login')
    else:
        return render_template('register.html', title = title)


# log out route with flash message

@app.route('/logout')
def logout():
    current_user = session.get('user')
    flash("You have been logged out!", "danger")
    session.pop("user", None)
    session.pop("email", None)
    session.pop("password", None)

    return redirect(url_for("home"))