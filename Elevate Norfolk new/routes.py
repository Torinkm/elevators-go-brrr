from __main__ import app

from flask import Flask,render_template,flash,redirect,url_for,session,request

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


@app.route('/accessibility')
def accessibility():
    current_user = session.get('user')

    return render_template("accessibility.html", current_user=current_user)

@app.route('/contact')
def contact():
    current_user = session.get('user')
    admin = session.get('admin')
    return render_template("contact.html", current_user=current_user)

@app.route('/about')
def about():
    current_user = session.get('user')
    admin = session.get('admin')
    return render_template("about.html", current_user=current_user)

@app.route('/hire', methods = ['POST', 'GET'])
def hire():
    current_user = session.get('user')
    if current_user:
        userID = db.queryDB('SELECT UserID FROM Users WHERE Username = ?', [current_user])[0][0]
    else:
        userID = -1

    if request.method == 'POST':    #   Find the right data if a search has been done
        searchData = request.form['Search']
        data = db.queryDB(f'SELECT * FROM Equipment_hire WHERE equipmentName LIKE "%{searchData}%"', [])
        if searchData:
            search = searchData
        else:
            search = False

    else:   #   Give all of the equipment data
        search = False
        data = db.queryDB(f'SELECT * FROM Equipment_hire')

    return render_template(
        'hire.html',
        current_user = session.get('user'),
        userID = userID,
        data = data,
        footer = True,
        search = search,
        admin = session.get('admin')
    )


@app.route('/hire_equipment/<int:hireID>')
def hire_equipment(hireID):
    current_user = session.get('user')
    if current_user:
        user_ID = db.queryDB('SELECT * FROM Users WHERE Username = ?', [current_user])[0][0]
        hireData = db.queryDB('SELECT * FROM Equipment_hire WHERE hireID = ?', [hireID])[0]
        if not hireData[7]:
            db.updateDB('UPDATE Equipment_hire SET CustomerID = ? WHERE hireID = ?', [user_ID, hireData[0]])
        else:
            if user_ID == hireData[7]:
                db.updateDB('UPDATE Equipment_hire SET CustomerID = NULL WHERE hireID = ?', [hireData[0]])
    else:
        flash('Please log in to book a session')
        return redirect(url_for('login'))


@app.route('/create_hire', methods = ['POST'])
def create_hire():
    if request.method == 'POST':
        if session.get('admin'):
            name = request.form['equipmentName']
            start_date =datetime.datetime.strptime(request.form['hire_start_date'], '%Y-%m-%d').strftime('%d/%m/%Y')
            end_date =datetime.datetime.strptime(request.form['hire_end_date'], '%Y-%m-%d').strftime('%d/%m/%Y')
            shortDesc = request.form['equipmentShortDescription']
            longDesc = request.form['equipmentLongDescription']
            db.updateDB('''INSERT INTO Equipment_hire(equipmentName, hire_start_date, hire_end_date, equipmentShortDescription, equipmentLongDescription)
            VALUES (?,?,?,?,?)''', [name, start_date, end_date, shortDesc, longDesc])
            return redirect(url_for('hire'))
        else:
            flash('Only admins can do this task.')
    else:
        return redirect(url_for('home'))

#   Admin Functionality   #


@app.route('/delete_equipment/<int:hireID>')
def delete_hire(hireID):
    if session.get('admin'):
        db.updateDB('DELETE FROM Equipment_hire WHERE hireID = ?', [hireID])
        flash('Successfully deleted Equipment', 'success')
        return redirect(url_for('hire'))

    else:
        flash('Only admins can do this task.', 'danger')
        return redirect(url_for('home'))
