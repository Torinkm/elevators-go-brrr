from __main__ import app

from flask import Flask, render_template, flash, redirect, url_for, request, session
from forms import NameForm,LoginForm
from db_connector import database
import requests
import hashlib
import datetime

#define db as database
db = database()

@app.route('/user')
def user():
    current_user = session.get('user')
    if not current_user:
        flash('You are not signed in, please sign in to use this feature.')
        return redirect(url_for('home'))

    return redirect(url_for('progressTracker'))

@app.route('/user/progress')
def progressTracker():
    current_user = session.get('user')
    if not current_user:
        flash('You are not signed in, please sign in to use this feature.')
        return redirect(url_for('home'))

    return render_template(
        'progressTracker.html',
        current_user = current_user,
        data = db.queryDB('SELECT * FROM users WHERE Username = ?', [current_user]),
        admin = session.get('admin')
    )

@app.route('/user/details', methods = ['POST', 'GET'])
def userDetails():
    current_user = session.get('user')

    #   Check that someone is logged in to use this page
    if not current_user:
        flash('You are not signed in, please sign in to use this feature.')
        return redirect(url_for('home'))

    if request.method == 'POST':
    
        #   Grab the password and hash it to compare with current password
        password = request.form['password']
        hashedPassword = hashlib.md5(str(password).encode()).hexdigest()

        #   Grab all the data
        newUsername = request.form['username']
        newEmail = request.form['email']
        newPassword = request.form['newPassword']
        confirmPassword = request.form['confirmPassword']

        #   Find the current users data in the table
        data = db.queryDB('SELECT * FROM users WHERE Username = ?', [current_user])[0]

        if hashedPassword == data[3]:

            #   Check if username is being changed
            if newUsername != data[1]: usernameChange = True
            else:                      usernameChange = False
            
            #   Check if email is being changed
            if newEmail != data[2]: emailChange = True
            else:                   emailChange = False
            
            #   Check if password is being changed
            if newPassword: passwordChange = True
            else:           passwordChange = False

            #   Change the username
            if usernameChange:
                #   Check if the username is not being used anywhere
                result = db.queryDB("SELECT * FROM users WHERE Username = ?", [newUsername])
                if result:
                    flash('Username already in use', 'danger')
                    return redirect(url_for('userDetails'))
                
                #   Update the name in the database
                db.updateDB('UPDATE Users SET Username = ? WHERE UserID = ?', [newUsername, data[0]])
                session['user'] = newUsername
                flash('Successfully changed username.', 'success')
            
            #   Change the email
            if emailChange:
                #   Check that the email is not being used anywhere
                result = db.queryDB("SELECT * FROM users WHERE Email = ?", [newEmail])
                if result:
                    flash('Email already in use', 'danger')
                    return redirect(url_for('userDetails'))
                
                #   Update the email in the database
                db.updateDB('UPDATE Users SET Email = ? WHERE UserID = ?', [newEmail, data[0]])
                session['email'] = newEmail
                flash('Successfully changed email.', 'success')

            #   Change the password
            if newPassword:
                #   Check if the passwords match
                if newPassword != confirmPassword:
                    flash('New passwords do not match', 'danger')
                    return redirect(url_for('userDetails'))
                
                #   Hash the new password
                newHashedPassword = hashlib.md5(str(newPassword).encode()).hexdigest()

                #   Update the email in the database
                db.updateDB('UPDATE Users SET Password = ? WHERE UserID = ?', [newHashedPassword, data[0]])
                flash('Successfully changed password')
            
        else:
            flash('The password you entered does not match your current password. Please try again.', 'danger')

        return redirect(url_for('userDetails'))

    else:

        return render_template(
            'accountDetails.html',
            current_user = current_user,
            data = db.queryDB('SELECT * FROM users WHERE Username = ?', [current_user]),
            admin = session.get('admin')
        )

@app.route('/user/delete', methods = ['POST', 'GET'])
def deleteUser():
    current_user = session.get('user')

    #   Check that someone is logged in to use this page
    if not current_user:
        flash('You are not signed in, please sign in to use this feature.')
        return redirect(url_for('home'))

    if request.method == 'POST':
        try:
            confirm = request.form['confirm']
            password = request.form['password']
            hashed_password = hashlib.md5(str(password).encode()).hexdigest()
            user = db.queryDB('SELECT * FROM Users WHERE Username = ?', [current_user])
            if user[0][3] == hashed_password:

                db.updateDB('DELETE FROM Users WHERE Username = ?', [current_user])
                flash('Successfully deleted account', 'success')
                session.pop('user', None)
                session.pop('email', None)
                session.pop('admin', None)
                return redirect(url_for('home'))

            flash('Incorrect password', 'danger')
            return redirect(url_for('deleteUser'))
        except:
            flash('Please tick the box', 'danger')
            return redirect(url_for('deleteUser'))
        
    
    return render_template(
        'deleteUser.html',
        current_user = current_user,
        admin = session.get('admin')
    )
    