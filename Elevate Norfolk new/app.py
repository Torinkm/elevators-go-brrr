from flask import Flask, session, flash

from datetime import timedelta, datetime
#importing database will allow us access the databases from the db_connector file
from db_connector import database

#define db as database
db = database()

app = Flask(__name__)
app.config['MESSAGE_FLASHING_OPTIONS'] = {'duration': 5}
app.secret_key = "hello"
app.permanent_session_lifetime = timedelta(minutes = 5)# our login session lasts 5 minutes before logging out for inactivity

# all routes imported from seperate files
import routes, user_page_routes, account_routes

if __name__ == '__main__':
   app.run(debug=True)   

