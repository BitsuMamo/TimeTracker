import os
import sqlite3

from datetime import datetime
from sqlite3.dbapi2 import Connection, Cursor
from typing import Dict, List, Optional, Tuple

# Constansts
DB_PATH = "activity.db"
DATE_FORMAT = "%Y-%m-%d"

# Prefixed with 'm' to show it's a global variable
m_db_con: Optional[Connection] = None

# Get a db connection. Initializes the db if the db is being accesed for the first time
def get_db_cursor() -> Cursor:
    global m_db_con
    if not os.path.exists(DB_PATH):
        with open(DB_PATH, "w") as file:
            file.close()
        m_db_con = sqlite3.connect(DB_PATH)
        print
        init_db(m_db_con)
        return m_db_con.cursor()
    if not m_db_con:
        m_db_con = sqlite3.connect(DB_PATH)
    return m_db_con.cursor()

def commit():
    global m_db_con
    m_db_con.commit()

def close_db_connection() -> None:
    global m_db_con
    if m_db_con is not None:
        m_db_con.close()


# Creates the main table in the db
def init_db(db_con: Connection) -> None:
    db_con.cursor().execute(
        "CREATE TABLE IF NOT EXISTS activities (application text, start_date text, end_date text)"
    )


# Adds the current activity values into the db
def save_to_db(activity_data: List[Tuple[str, datetime, datetime]]) -> None:
    conn = get_db_cursor()
    conn.executemany(
        "INSERT INTO activities VALUES (?, ?, ?)",
        [
            (entry[0], entry[1].isoformat(), entry[2].isoformat())
            for entry in activity_data
        ],
    )
    commit()
    


# Returns all the acitvites logged in the database
def get_all_data() -> List[Tuple[str, datetime, datetime]]:
    conn = get_db_cursor()
    data = conn.execute("SELECT * FROM activities ORDER BY start_date ASC").fetchall()
    return [
        (entry[0], datetime.fromisoformat(entry[1]), datetime.fromisoformat(entry[2]))
        for entry in data
    ]

