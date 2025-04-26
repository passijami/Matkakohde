import sqlite3
from flask import Flask
from flask import abort, redirect, render_template, request, session, flash
import db
import config
import items
import users
import re

app = Flask(__name__)
app.secret_key = config.secret_key

def check_login():
    if "user_id" not in session:
        abort(403)

@app.route("/")
def index():
    all_items = items.get_items()
    return render_template("index.html", items=all_items)

@app.route("/user/<int:user_id>")
def show_user(user_id):
    user = users.get_user(user_id)
    if not user:
        abort(404)
    items = users.get_items(user_id)
    return render_template("show_user.html", user=user, items=items)


@app.route("/find_item")
def find_item():
    query = request.args.get("query")
    if query:
        results = items.find_items(query)
    else:
        query = ""
        results = []
    return render_template("find_item.html", query=query, results=results)

@app.route("/item/<int:item_id>")
def show_item(item_id):
    item = items.get_item(item_id)
    if not item:
        abort(404)
    classes = items.get_classes(item_id)
    return render_template("show_item.html", item=item, classes=classes)

@app.route("/new_item")
def new_item():
    check_login()
    classes = items.get_all_classes()
    return render_template("new_item.html", classes=classes)

@app.route("/create_item", methods=["POST"])
def create_item():
    check_login()

    title = request.form["title"]
    if not title or len(title) > 50:
        abort(403, "Otsikko ei kelpaa!")
    description = request.form["description"]
    if not description or len(description) > 1000:
        abort(403, "Kuvaus ei kelpaa!")
    budget = request.form["budget"]
    if not re.search("^[1-9][0-9]{0,5}$", budget):
        abort(403, "Budjetti ei kelpaa!")
    user_id = session["user_id"]

    all_classes = items.get_all_classes()

    classes = []
    for entry in request.form.getlist("classes"):
        if entry:
            my_title, my_value = entry.split(":")
            if my_title not in all_classes:
                abort(403)
            if my_value not in all_classes[my_title]:
                abort(403)
            classes.append((my_title, my_value))

    items.add_item(title, description, budget, user_id, classes)

    return redirect("/")

@app.route("/edit_item/<int:item_id>")
def edit_item(item_id):
    check_login()
    item = items.get_item(item_id)
    if not item:
        abort(404)
    if item["user_id"] != session["user_id"]:
        abort(403)
    all_classes = items.get_all_classes()
    classes = {}
    for my_class in all_classes:
        classes[my_class] = ""
    for entry in items.get_classes(item_id):
        classes[entry["title"]] = entry["value"]

    return render_template("edit_item.html", item=item, classes=classes, all_classes=all_classes)

@app.route("/update_item", methods=["POST"])
def update_item():
    check_login()
    item_id = request.form["item_id"]
    item = items.get_item(item_id)
    if not item:
        abort(404)
    if item["user_id"] != session["user_id"]:
        abort(403)

    title = request.form["title"]
    if not title or len(title) > 50:
        abort(403, "Otsikko ei kelpaa!")
    description = request.form["description"]
    if not description or len(description) > 1000:
        abort(403, "Kuvaus ei kelpaa!")

    classes = []
    all_classes = items.get_all_classes()
    for entry in request.form.getlist("classes"):
        if entry:
            my_title, my_value = entry.split(":")
            if my_title not in all_classes:
                abort(403)
            if my_value not in all_classes[my_title]:
                abort(403)
            classes.append((my_title, my_value))

    items.update_item(item_id, title, description, classes)

    return redirect("/item/" + str(item_id))

@app.route("/remove_item/<int:item_id>", methods=["GET", "POST"])
def remove_item(item_id):
    check_login()
    item = items.get_item(item_id)
    if not item:
        abort(404)
    if item["user_id"] != session["user_id"]:
        abort(403)

    if request.method == "GET":
        return render_template("remove_item.html", item=item)
    if request.method == "POST":
        items.remove_item(item_id)
        return redirect("/")
    else:
        return redirect("/item/" + str(item_id))

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        return "VIRHE: salasanat eivät ole samat"
    try:
        users.create_user(username, password1)
    except sqlite3.IntegrityError:
        return "VIRHE: tunnus on jo varattu"
    flash("VIRHE: väärä tunnus tai salasana")
    return redirect("/")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST": 
        username = request.form["username"]
        password = request.form["password"]

        user_id = users.check_login(username, password)
        if user_id:
            session["user_id"] = user_id
            session["username"] = username
            return redirect("/")
        else:
            #return "VIRHE: väärä tunnus tai salasana"
            flash("VIRHE: väärä tunnus tai salasana")
            return redirect("/login")
    
@app.route("/add_favorite", methods=["POST"])
def add_favorite():
    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]
    item_id = request.form["item_id"]

    sql = "INSERT INTO favorites (user_id, item_id) VALUES (?, ?)"
    db.execute(sql, [user_id, item_id])

    return redirect("/")

@app.route("/favorites")
def favorites():
    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]

    sql = """SELECT items.id, items.title
             FROM items
             JOIN favorites ON items.id = favorites.item_id
             WHERE favorites.user_id = ?"""
    suosikit = db.query(sql, [user_id])

    return render_template("favorites.html", favorites=suosikit)

@app.route("/logout")
def logout():
    if "user_id" in session:
        del session["user_id"]
        del session["username"]
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
