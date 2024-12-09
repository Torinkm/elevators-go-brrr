#   Imports   #

from flask import Flask, render_template, flash, redirect, url_for, request, session
from forms import NameForm, LoginForm
from db_connector import database
import hashlib
import datetime

from __main__ import app, db

#   Routes   #

@app.route('/advice', methods = ['POST', 'GET'])
def advices():

    if request.method == 'POST':
        search = request.form['Search']
        adviceType = request.form['adviceType']
        if adviceType == 'Any':
            data = db.queryDB(f'SELECT * FROM Advice WHERE AdviceName LIKE "%{search}%"', [])
        else:
            data = db.queryDB(f'SELECT * FROM Advice WHERE AdviceName LIKE "%{search}%" AND AdviceType = ?', [adviceType])
    
    else:
        data = db.queryDB('SELECT * FROM Advice')
        adviceType = 'Any'
        search = False

    return render_template('advice.html', 
        current_user = session.get('user'),
        data = data,
        footer = True,
        search = search,
        adviceType = adviceType,
        admin = session.get('admin'))

@app.route('/create_advice', methods= ['POST', 'GET'])
def create_advice():
    if request.method == 'POST':
        if session.get('admin'):
            name = request.form['AdviceName']
            advice_type = request.form['AdviceType']
            shortDesc = request.form['AdviceShortDescription']
            longDesc = request.form['AdviceLongDescription']
            db.updateDB('''INSERT INTO Advice(AdviceName, AdviceDesc, AdviceShortDesc, AdviceType)
            VALUES (?,?,?,?)''', [name, longDesc, shortDesc, advice_type])
            return redirect(url_for('advices'))
        
        else:
            flash('Only admins can do this task.')
    else:
        return redirect(url_for('home'))

#   Admin functionality   #

@app.route('/delete_advice/<int:adviceID>')
def delete_advice(adviceID):
    if session.get('admin'):
        db.updateDB('DELETE FROM Advice WHERE AdviceID = ?', [adviceID])
        flash('Successfully deleted advice', 'success')
        return redirect(url_for('advices'))
    
    else:
        flash('Only admins can do this task.', 'danger')
        return redirect(url_for('home'))
    