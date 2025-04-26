CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE items (
    id INTEGER PRIMARY KEY,
    title TEXT,
    description TEXT,
    budget INTEGER,
    user_id INTEGER REFERENCES users
);

CREATE TABLE classes (
    id INTEGER PRIMARY KEY,
    title TEXT,
    value TEXT
);

CREATE TABLE item_classes (
    id INTEGER PRIMARY KEY,
    item_id INTEGER REFERENCES items,
    title TEXT,
    value TEXT
);

CREATE TABLE favorites (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    item_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (item_id) REFERENCES items(id)
);
