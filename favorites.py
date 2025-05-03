import db
import sqlite3

def add_favorite(user_id, item_id):
    sql_check = "SELECT 1 FROM favorites WHERE user_id = ? AND item_id = ?"
    result = db.query(sql_check, [user_id, item_id])
    if result:
        return False
    
    sql = "INSERT INTO favorites (user_id, item_id) VALUES (?, ?)"
    db.execute(sql, [user_id, item_id])
    return True

def get_favorites(user_id):
    sql = """SELECT items.id, items.title
             FROM items
             JOIN favorites ON items.id = favorites.item_id
             WHERE favorites.user_id = ?"""
    return db.query(sql, [user_id])
