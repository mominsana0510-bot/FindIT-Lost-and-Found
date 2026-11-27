import sqlite3

DB_NAME = "findit_campus.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # User Credentials Schema
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    # Items Schema with Foreign Key Binding
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS items (
            item_id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            description TEXT NOT NULL,
            item_type TEXT NOT NULL,
            location TEXT NOT NULL,
            contact TEXT NOT NULL,
            user_id INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
    """)

    conn.commit()
    conn.close()


def register_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username.strip(), password.strip()),
        )
        conn.commit()
        return cursor.lastrowid
    except sqlite3.IntegrityError:
        return None
    finally:
        conn.close()


def authenticate_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT user_id FROM users WHERE username = ? AND password = ?",
        (username.strip(), password.strip()),
    )
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None


def add_item(title, category, description, item_type, location, contact, user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO items (title, category, description, item_type, location, contact, user_id)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (title, category, description, item_type, location, contact, user_id),
    )
    conn.commit()
    conn.close()


def fetch_filtered_items(search_query="", category="All", item_type="All"):
    conn = get_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM items WHERE 1=1"
    params = []

    if search_query.strip():
        query += " AND (title LIKE ? OR description LIKE ?)"
        params.extend([f"%{search_query}%", f"%{search_query}%"])

    if category != "All":
        query += " AND category = ?"
        params.append(category)

    if item_type != "All":
        query += " AND item_type = ?"
        params.append(item_type)

    query += " ORDER BY item_id DESC"
    cursor.execute(query, params)
    records = cursor.fetchall()
    conn.close()
    return records


def delete_item(item_id, current_user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM items WHERE item_id = ? AND user_id = ?",
        (item_id, current_user_id),
    )
    conn.commit()
    conn.close()
