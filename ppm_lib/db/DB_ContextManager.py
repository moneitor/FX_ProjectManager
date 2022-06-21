import sqlite3

class DBConnection:
    """ Returns a connection to a database, and after
    the process has been run, it will commit and close the file
    """
    def __init__(self, db):
        self.connection = None
        self.db = db

    def __enter__(self):
        self.connection = sqlite3.connect(self.db)
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.commit()
        self.connection.close()