from dotenv import load_dotenv
import os
import MySQLdb
from members import nickToName

load_dotenv()

class db:
    """Highly customized db class for the purposes of this bot. Loads of very specific helper functions to wrap the mess of db handling away."""

    _instance = None

    def __init__(self):

        try:                                                                                                                 
            host = os.getenv("db_host")
            user = os.getenv("db_user")
            pw = os.getenv("db_password")
            dbname = os.getenv("db")
            dbconn = MySQLdb.connect(host, user, pw, dbname)
            print("Database connection established.")
        except:
            print("Failed to connect to database. Aborting.")
            exit()

        db._instance = dbconn

        return

    @staticmethod
    def getdb():
        if(db._instance == None):
            db()

        return db._instance

    def newRankings(id, members):
        c = db.getdb().cursor()
        c.execute(f"DELETE FROM rankings WHERE user={id}")
        
        for rank, m in enumerate(members):
            c.execute(f"INSERT INTO rankings VALUES({id}, '{nickToName(m)}', {rank+1})")

        db.getdb().commit()

        return

    def getRankings(id):
        c = db.getdb().cursor()
        c.execute(f"SELECT * FROM rankings WHERE user={id} ORDER BY ranking")
        return c.fetchall()

