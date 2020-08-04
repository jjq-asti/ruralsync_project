#!/usr/bin/python3

import sqlite3 as db

def connectDB(dbname):
    conn = db.connect(dbname)
    return conn

    
class Files(db.Cursor):
    def __init___(self, connection = None):
        super().__init__(connection)

    def createTable(self):
        tableName = "files"
        self.execute("CREATE TABLE IF NOT EXiSTS {} (".format(tableName) + \
        "id INTEGER PRIMARY KEY AUTOINCREMENT,"    \
        "name TEXT NOT NULL,"   \
        "extension TEXT NOT NULL,"  \
        "date TEXT NOT NULL,"   \
        "size TEXT NOT NULL," \
        "directory TEXT NOT NULL,"  \
        "owner TEXT NOT NULL,"   \
        "carousel INTEGER NOT NULL," \
        "UNIQUE (name)" \
        ")"
        )

    def insertData(self,data):
        self.execute("INSERT OR IGNORE INTO files(name,extension,date,size,directory,owner,carousel) VALUES (?,?,?,?,?,?,?)",data)
        return self.lastrowid

    def insertDataMulti(self,data):
        self.executemany("INSERT INTO {} VALUES",arry_of_tuples_type)
    
    def getDataUsingId(self,id):
        self.execute("SELECT * FROM files WHERE id=?",(id,))
        return self.fetchone()
    def getAllData(self):
        self.execute("SELECT * FROM files")
        return self.fetchall()
    def updateCarousel(self,id,carousel):
        self.execute("UPDATE files SET carousel = ? WHERE id=?",(carousel,id,))
    def getCarouselStatus(self,id):
        self.execute("SELECT carousel FROM files WHERE id=?",(id,))
        return self.fetchone()
    def removeRecord(self,id):
        self.execute("DELETE FROM files WHERE id=?",(id,))

    def updateData():
        self.execute()
    def dropTable(self,tableName):
        self.execute("DROP TABLE {}".format(tableName))

    

if __name__ == "__main__":
    conn = connectDB("test.db")
    file_db = Files(conn)
    file_db.createTable()
    #rows = file_db.getDataUsingId(4)
    #for i in rows:
    #    print(i)
    conn.close()
