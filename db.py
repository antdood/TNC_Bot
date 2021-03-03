from dotenv import load_dotenv
import os
import MySQLdb
from members import nickToName
import operator

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
            dbconn.ping(True)
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

        # MySQL has no clean UPSERT so we just delete and reinsert ¯\_(ツ)_/¯
        c.execute(f"DELETE FROM rankings WHERE user={id}")
        
        for rank, m in enumerate(members):
            c.execute(f"INSERT INTO rankings VALUES({id}, '{nickToName(m)}', {rank+1})")

        db.getdb().commit()

        return

    def getRankings(id):
        c = db.getdb().cursor()
        c.execute(f"SELECT member,ranking FROM rankings WHERE user={id} ORDER BY ranking")
        return c.fetchall()

    def shiftRanking(user, nick, operation, amount):
        # These aren't the other way round, we're dealing with rankings. Unintuitive, I know.
        ops = {
            '+' : operator.sub,
            '-' : operator.add
        }

        c = db.getdb().cursor()
        name = nickToName(nick)

        c.execute(f"SELECT ranking FROM rankings WHERE user={user} AND member='{name}'")

        oldRank = c.fetchone()[0]

        newRank = ops[operation](oldRank, amount)

        newRank = min(max(newRank, 1), 9)

        # Can be a little clever with ternaries here but ¯\_(ツ)_/¯
        if(operation == '+'):
            c.execute(f"UPDATE rankings SET ranking = ranking + 1 WHERE user={user} AND ranking>={newRank} AND ranking<{oldRank}")
        else:
            c.execute(f"UPDATE rankings SET ranking = ranking - 1 WHERE user={user} AND ranking<={newRank} AND ranking>{oldRank}")
        c.execute(f"UPDATE rankings SET ranking = {newRank} WHERE user={user} AND member='{name}'")
        
        db.getdb().commit()

