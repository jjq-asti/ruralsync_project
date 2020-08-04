#!/usr/bin/python3

import sqlite3 as db

def connectDB(dbname):
    conn = db.connect(dbname)
    return conn

    
class Files(sql.Cursor):
    def __init___(self, connection = None):
        super().__init__(connection)

    def createTable(self):
        tableName = "files"
        self.execute("CREATE TABLE IF NOT EXiSTS {} (".format(tableName) + \
        "id INTEGER PRIMARY KEY AUTOINCREMENT,"    \
        "name TEXT NOT NULL,"   \
        "extension TEXT NOT NULL,"  \
        "date TEXT NOT NULL,"   \
        "directory TEXT NOT NULL,"  \
        "owner TEXT NOT NULL"   \
        ")"
        )

    def insertData(self,data):
        self.execute("INSERT INTO {} VALUES (?,?,?,?,?)",[values,])

    def insertDataMulti(self,data):
        self.executemany("INSERT INTO {} VALUES",arry_of_tuples_type)

    def updateData():
        self.execute()
    def dropTable(self,tableName):
        self.execute("DROP TABLE {}".format(tableName))

    

if __name__ == "__main__":
    conn = connectDB("test.db")
    file_db = Files(conn)
    file_db.createTable()
    conn.close()
