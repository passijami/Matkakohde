import db

def add_item(title, description, budget, user_id):
    sql = "INSERT INTO items (title, description, budget, user_id) VALUES (?, ?, ?, ?)"
    db.execute(sql, [title, description, budget, user_id])
