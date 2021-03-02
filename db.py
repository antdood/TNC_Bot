from dotenv import load_dotenv
import os
import MySQLdb

load_dotenv()

class db:
    _instance = None

    def __init__(self):

        try:                                                                                                                                                                                                                                                                            
            db = MySQLdb.connect("antdoodawck.mysql.pythonanywhere-services.com", "antdoodawck", os.getenv("sql_password"), "antdoodawck$TNC_Data")
            print("Database connection established.")
        except:
            print("Failed to connect to database. Aborting.")
            exit()

        db._instance = self

        return

    @staticmethod
    def getdb(self):
        if(db._instance == None):
            db()

        return db._instance
