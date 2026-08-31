import sqlite3

def get_conn():
    return sqlite3.connect("database.db")

def init_db():
    conn = get_conn()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS campaigns (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            brief TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS generations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            campaign_id INTEGER,
            text TEXT,
            status TEXT DEFAULT 'pending',   -- pending / approved / rejected
            parent_id INTEGER                -- links an "improve" back to the original
        )
    """)
    conn.commit()
    conn.close()

def save_generation(campaign_id, text, parent_id=None):
    conn = get_conn()
    cur = conn.execute(
        "INSERT INTO generations (campaign_id, text, parent_id) VALUES (?, ?, ?)",
        (campaign_id, text, parent_id)
    )
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    return new_id


def get_generations(campaign_id):
    conn = get_conn()
    cur = conn.execute(
        "SELECT id, text, status FROM generations WHERE campaign_id = ?",
        (campaign_id,)
    )
    rows = cur.fetchall()
    conn.close()
    return rows

def update_status(generation_id, status):
    conn = get_conn()
    conn.execute(
        "UPDATE generations SET status = ? WHERE id = ?",
        (status, generation_id)
    )
    conn.commit()
    conn.close()