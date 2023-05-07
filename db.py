import sqlite3
import os

class Database:
    def __init__(self, filepath: str):
        if not os.path.exists(filepath): # If the DB file does not exist, create one
            dbFile = open(filepath, "w")
            dbFile.close()
        self.connection = sqlite3.connect(filepath)
        self.cursor = self.connection.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS UTC (ID INTEGER NOT NULL PRIMARY KEY, OFFSET INTEGER)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS BIRTHDAY (ID INTEGER NOT NULL PRIMARY KEY, MONTH INTEGER, DAY INTEGER)")
        self.connection.commit()
    
    def insertUTC(self, memberId: int, UTCOffset: int) -> None:
        if self.cursor.execute("SELECT * FROM UTC WHERE ID = ?", (memberId,)).fetchone():
            self.cursor.execute("UPDATE UTC SET OFFSET = ? WHERE ID = ?", (UTCOffset, memberId,))
        else:    
            self.cursor.execute("INSERT INTO UTC VALUES(?, ?)", (memberId, UTCOffset,))
        self.connection.commit()
    
    def getUTC(self, memberId: int) -> tuple: # Fix this
        result = self.cursor.execute("SELECT OFFSET FROM UTC WHERE ID = ?", (memberId,))
        return result.fetchone()
    
    def insertBirthday(self, memberId: int, month: int, day: int) -> None:
        if self.cursor.execute("SELECT * FROM BIRTHDAY WHERE ID = ?", (memberId,)).fetchone():
            self.cursor.execute("UPDATE BIRTHDAY SET MONTH = ?, DAY = ? WHERE ID = ?", (month, day, memberId,))
        else:
            self.cursor.execute("INSERT INTO BIRTHDAY VALUES(?, ?, ?)", (memberId, month, day,))
        self.connection.commit()
    
    def getBirthday(self, memberId: int) -> tuple:
        result = self.cursor.execute("SELECT MONTH, DAY FROM BIRTHDAY WHERE ID = ?", (memberId,))
        return result.fetchone()
    
    def getAllBirthdays(self) -> list[tuple]:
        results = self.cursor.execute("SELECT * FROM BIRTHDAY")
        return results.fetchall()