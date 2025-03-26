import sqlite3
from flask import g

def get_connection():
    con = sqlite3.connect("database.db")
    con.execute("PRAGMA foreign_keys = ON")
    con.row_factory = sqlite3.Row
    return con

def execute(sql, params=[]):
    con = get_connection()
    try:
        result = con.execute(sql, params)
        g.last_insert_id = result.lastrowid

        con.commit()
        
    except sqlite3.Error as e:
        con.rollback()
        raise e
    finally:
        con.close()

def last_insert_id():
    return getattr(g, 'last_insert_id', None)

def query(sql, params=[]):
    con = get_connection()
    try:
        result = con.execute(sql, params).fetchall()
    except sqlite3.Error as e:
        raise e
    finally:
        con.close()
    return result