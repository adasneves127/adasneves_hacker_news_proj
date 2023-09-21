import sqlite3


class db_conn:

    def __init__(self, db_name: str):
        self.db = sqlite3.connect(db_name)
