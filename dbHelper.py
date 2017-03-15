import sqlite3


class DBHelper:

    #__init__() takes a database name and creates a db connection
    def __init__(self, dbname="qa.sqlite"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname)

    #setup() creates a new table 'commandlog' in our db. This table has 2 columns (recent- for recent queries, owner - stores chat_id)
    def setup(self):
        tblstmt = "CREATE TABLE IF NOT EXISTS log (recent text, owner text)"
        ownidx = "CREATE INDEX IF NOT EXISTS ownIndex ON log (owner ASC)"
        recentidx = "CREATE INDEX IF NOT EXISTS recentIndex ON log (recent ASC)"
        self.conn.execute(tblstmt)
        self.conn.execute(ownidx)
        self.conn.execute(recentidx)
        self.conn.commit()

    #adds the query to database
    def add_query(self, text, owner):
        stmt = "INSERT INTO log (recent, owner) VALUES (?, ?)"
        args = (text, owner)
        self.conn.execute(stmt, args)
        self.conn.commit()

    #sends queries of all users 
    def all_query(self):
        stmt = "SELECT DISTINCT recent FROM log"
        return [x[0] for x in self.conn.execute(stmt)]
    
    #sends queries of a particular user
    def user_query(self, owner):
        stmt = "SELECT DISTINCT recent FROM log WHERE owner = (?)"
        args = (owner, )
        return [x[0] for x in self.conn.execute(stmt, args)]

            



