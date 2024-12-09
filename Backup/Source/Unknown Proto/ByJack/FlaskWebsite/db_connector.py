import sqlite3

class database():

    #   Defines our database "gamesShopDB.db"
    def __init__(self):
        self.DBname = 'a.db'

    #   Create our database connection
    def connect(self):
        conn = None
        try:
            conn = sqlite3.connect(self.DBname)
        except Exception() as e:
            print(e)
        return conn
    
    #   Close our database
    def disconnect(self, conn):
        conn.close()
    
    #   Query the database, and return the result
    def queryDB(self, command, params = []):
        conn = self.connect()
        cur = conn.cursor()
        cur.execute(command, params)

        result = cur.fetchall()

        self.disconnect(conn)
        return result
    
    #   Updates the database
    def updateDB(self, command, params = []):
        conn = self.connect()
        cur = conn.cursor()
        cur.execute(command, params)
        conn.commit()
        result = cur.fetchall()
        self.disconnect(conn)
        return result