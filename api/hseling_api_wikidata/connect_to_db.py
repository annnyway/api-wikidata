import sqlite3

def connect(path_to_db):
    conn = sqlite3.connect(path_to_db)
    cursor = conn.cursor()
    return cursor