#   Imports   #

from flask import Flask, render_template, flash, redirect, url_for, request, session
from forms import NameForm, LoginForm
from db_connector import database
import hashlib
import datetime

from __main__ import app, db

#   Routes   #

@app.route('/sessions', methods = ['POST', 'GET'])
def sessions():
    current_user = session.get('user')
    if current_user:
        userID = db.queryDB('SELECT UserID FROM Users WHERE Username = ?', [current_user])[0][0]
    else:
        userID = -1

    if request.method == 'POST':    #   Find the right data if a search has been done
        searchData = request.form['Search']
        data = db.queryDB(f'SELECT * FROM Sessions WHERE SessionName LIKE "%{searchData}%"', [])
        if searchData:
            search = searchData
        else:
            search = False

    else:   #   Give all of the session data
        search = False
        data = db.queryDB(f'SELECT * FROM Sessions')

    return render_template(
        'sessions.html',
        current_user = session.get('user'),
        userID = userID,
        data = data,
        footer = True,
        search = search,
        admin = session.get('admin')
    )

@app.route('/book_session/<int:sessionID>')
def book_session(sessionID):
    current_user = session.get('user')
    if current_user:
        user_ID = db.queryDB('SELECT * FROM Users WHERE Username = ?', [current_user])[0][0]
        sessionData = db.queryDB('SELECT * FROM Sessions WHERE SessionID = ?', [sessionID])[0]
        if not sessionData[7]:  #   Booking the session
            db.updateDB('UPDATE Sessions SET CustomerID = ? WHERE SessionID = ?', [user_ID, sessionData[0]])
            flash('Successfully booked the session.', 'success')
        else:
            if user_ID == sessionData[7]:   #   Unbooking the session
                db.updateDB('UPDATE Sessions SET CustomerID = NULL WHERE SessionID = ?', [sessionData[0]])
                flash('Successfully unbooked session.', 'success')
            else:   #   Unbooking session when you are not the one booked in
                flash('You cannot unbook someone else\'s session', 'danger')
        return redirect(url_for('sessions'))
    else:
        flash('Please log in to book a session')
        return redirect(url_for('login'))

@app.route('/create_session', methods = ['POST'])
def create_session():
    if request.method == 'POST':
        if session.get('admin'):
            name = request.form['SessionName']
            date =datetime.datetime.strptime(request.form['SessionDate'], '%Y-%m-%d').strftime('%d/%m/%Y')
            time = request.form['SessionTime']
            duration = request.form['SessionDuration']
            shortDesc = request.form['SessionShortDescription']
            longDesc = request.form['SessionLongDescription']
            db.updateDB('''INSERT INTO Sessions(SessionName, SessionDate, SessionTime, SessionDuration, SessionShortDescription, SessionLongDescription)
            VALUES (?,?,?,?,?,?)''', [name, date, time, duration, shortDesc, longDesc])
            flash('Successfully created session', 'success')
            return redirect(url_for('sessions'))
        
        else:
            flash('Only admins can do this task.')
    else:
        return redirect(url_for('home'))

#   Admin Functionality   #

@app.route('/delete_session/<int:sessionID>')
def delete_session(sessionID):
    if session.get('admin'):
        db.updateDB('DELETE FROM Sessions WHERE SessionID = ?', [sessionID])
        flash('Successfully deleted session', 'success')
        return redirect(url_for('sessions'))
    
    else:
        flash('Only admins can do this task.', 'danger')
        return redirect(url_for('home'))
    