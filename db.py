import sqlite3

def get_conn():
    return sqlite3.connect("database.db")

print(get_conn())
# def init_db():
    # conn = get_conn()
