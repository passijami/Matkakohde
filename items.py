import db

def add_item(title, description, budget, user_id):
    sql = "INSERT INTO items (title, description, budget, user_id) VALUES (?, ?, ?, ?)"
    db.execute(sql, [title, description, budget, user_id])

def get_items():
    sql = "SELECT id, title FROM items ORDER BY id DESC"
    return db.query(sql)

def get_item(item_id):
    sql = """SELECT items.id,
                    items.title,
                    items.description,
                    items.budget,
                    users.id AS user_id,
                    users.username
             FROM items
             JOIN users ON items.user_id = users.id
             WHERE items.id = ?"""
    result = db.query(sql, [item_id])
    return result[0] if result else None

def update_item(item_id, title, description):
    sql = """UPDATE items
             SET title = ?, description = ?
             WHERE id = ?"""
    db.execute(sql, [title, description, item_id])

def remove_item(item_id):
    sql = "DELETE FROM items WHERE id = ?"
    db.execute(sql, [item_id])

def find_items(query):
    sql = """SELECT id, title
             FROM items
             WHERE description LIKE ?
             ORDER BY id DESC"""
    like = "%" + query + "%"
    return db.query(sql, [like])
