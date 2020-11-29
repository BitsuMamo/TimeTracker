import os
import sqlite3

from datetime import date, datetime
from sqlite3.dbapi2 import Connection, Cursor
from time import time
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
    table_init_str = "".join(
        [
            "CREATE TABLE IF NOT EXISTS activities (application text, start_date_iso",
            " text, end_date_iso text, start_year integer, start_month integer, start_day integer,",
            " start_time text, end_year integer, end_month integer, end_day integer, end_time text)",
        ]
    )
    db_con.cursor().execute(table_init_str)


# Adds the current activity values into the db
def save_to_db(activity_data: List[Tuple[str, datetime, datetime]]) -> None:
    conn = get_db_cursor()
    formatted_data = [generate_values(entry) for entry in activity_data]
    conn.executemany(
        "INSERT INTO activities VALUES (?, ?, ?, ?, ?, ?, ?, ?, ? ,?, ?)",
        formatted_data,
    )
    commit()


DB_VALUE_TYPE = Tuple[str, str, int, int, int, str, str, int, int, int, str]


def generate_values(entry: Tuple[str, datetime, datetime]) -> DB_VALUE_TYPE:
    app_name = entry[0]
    start_date = entry[1]
    end_date = entry[2]
    return (
        app_name,
        start_date.isoformat(),
        end_date.isoformat(),
        start_date.year,
        start_date.month,
        start_date.day,
        f"{start_date.hour}:{start_date.minute}:{start_date.second}",
        end_date.year,
        end_date.month,
        end_date.day,
        f"{end_date.hour}:{end_date.minute}:{end_date.second}",
    )


# Returns all the acitvites logged in the database
def get_all_data() -> List[Tuple[str, datetime, datetime]]:
    conn = get_db_cursor()
    data = conn.execute(
        "SELECT * FROM activities ORDER BY start_date_iso ASC"
    ).fetchall()
    return [
        (entry[0], datetime.fromisoformat(entry[1]), datetime.fromisoformat(entry[2]))
        for entry in data
    ]

