import sqlite3
from typing import Dict


class Database:
    # This is a database to store message, each message contain username, and message

    def __init__(self, db_file):
        self.db_file = db_file
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

    def create_table(self):
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, message TEXT)"
        )
        self.conn.commit()

    def insert(self, username, message):
        self.cursor.execute(
            "INSERT INTO messages (username, message) VALUES (?, ?)",
            (username, message),
        )
        self.conn.commit()

    def get(self) -> Dict:
        self.cursor.execute("SELECT * FROM messages")
        # return in json format and sorted oldest to newest
        return [{"id": x[0], "username": x[1], "message": x[2]} for x in self.cursor]
