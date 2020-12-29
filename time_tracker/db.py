import os
import sqlite3

from datetime import datetime
from sqlite3.dbapi2 import Connection, Cursor
from time_tracker.types_and_constants import Record, DB_PATH, BASE_COMMAND
from typing import List, Optional, Tuple, Union

DB_VALUE_TYPE = Tuple[str, str, str, int, int, int, str, int, int, int, str]


class AppDB:
    # Prefixed with 'm' to show it's a global variable
    _con: Optional[Connection] = None

    # Dependency Injection. Used for testing
    def __init__(self, conn: Optional[Connection] = None) -> None:
        if conn:
            self._con = conn

    @property
    def conn(self) -> Connection:
        if self._con:
            return self._con
        else:
            if not os.path.exists(DB_PATH):
                self.init_db()
            self._con = sqlite3.connect(DB_PATH)
            return self._con

    # Get a db connection. Initializes the db if the db is being accesed for the first time
    def get_db_cursor(self) -> Cursor:
        return self.conn.cursor()

    # Should include a check to see if the file already exists
    # Creates the main table in the db
    def init_db(self, conn: Optional[Connection] = None) -> None:
        if not conn:
            with open(DB_PATH, "w") as file:
                file.close()
            temp_con = sqlite3.connect(DB_PATH)
        else:
            temp_con = conn
        table_init_str = "".join(
            [
                "CREATE TABLE IF NOT EXISTS activities (application text, start_date_iso",
                " text, end_date_iso text, start_year integer, start_month integer, start_day integer,",
                " start_time text, end_year integer, end_month integer, end_day integer, end_time text)",
            ]
        )
        temp_con.cursor().execute(table_init_str)

    # Adds the current activity values into the db
    def save(self, activity_data: Union[List[Record], Record]) -> None:
        COMMAND = "INSERT INTO activities VALUES (?, ?, ?, ?, ?, ?, ?, ?, ? ,?, ?)"
        conn = self.get_db_cursor()
        if isinstance(activity_data, list):
            formatted_data = [self.record_to_db_type(entry) for entry in activity_data]
            conn.executemany(
                COMMAND, formatted_data,
            )
        else:
            conn.execute(COMMAND, self.record_to_db_type(activity_data))
        self.conn.commit()

    def record_to_db_type(self, entry: Record) -> DB_VALUE_TYPE:
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

    def db_to_record(self, db_entry: DB_VALUE_TYPE) -> Record:
        data_list = [
            db_entry[0],
            datetime.fromisoformat(db_entry[1]),
            datetime.fromisoformat(db_entry[2]),
        ]
        return tuple(data_list)

    # Logic for generating the SQL command for date filtering
    def date_filtering(
        self, earliest_date: Optional[str] = None, latest_date: Optional[str] = None
    ) -> str:
        GREATER_THAN = "start_date_iso > "
        LESS_THAN = "start_date_iso < "
        my_command = ""
        if earliest_date or latest_date:
            my_command = "WHERE "
            if earliest_date and latest_date:
                my_command = my_command + GREATER_THAN + "?" + " AND " + LESS_THAN + "?"
            elif latest_date:
                my_command = my_command + LESS_THAN + "?"
            elif earliest_date:
                my_command = my_command + GREATER_THAN + "?"
        return my_command
    

    # Helps buidls the overall SQL command
    def base_command(self, additional: Optional[str] = None) -> str:
        if additional:
            return (
                "SELECT * FROM activities "
                + additional
                + " ORDER BY start_date_iso ASC"
            )
        else:
            return "SELECT * FROM activities ORDER BY start_date_iso ASC"

    # Functions for extracting data from the DB

    def get_all_data(self) -> List[Record]:
        conn = self.get_db_cursor()
        return [
            self.db_to_record(db_entry)
            for db_entry in conn.execute(BASE_COMMAND).fetchall()
        ]

    #
    def get_data_by_date(
        self, *, earliest_date: Optional[str] = None, latest_date: Optional[str] = None
    ) -> List[Record]:
        my_command = self.base_command(self.date_filtering(earliest_date, latest_date))
        conn = self.get_db_cursor()
        print(my_command)
        if earliest_date and latest_date:
            cursor = conn.execute(my_command, (earliest_date, latest_date))
        elif earliest_date:
            cursor = conn.execute(my_command, [earliest_date])
        elif latest_date:
            cursor = conn.execute(my_command, [latest_date])
        else:
            cursor = conn.execute(my_command)
        return [self.db_to_record(db_entry) for db_entry in cursor.fetchall()]

    def get_data_by_app(self, app: str) -> List[Record]:
        CONDITION = f" WHERE application LIKE '%{app}%'"
        conn = self.get_db_cursor()
        my_command = self.base_command(CONDITION)
        print(my_command)
        return [
            self.db_to_record(db_entry)
            for db_entry in conn.execute(my_command).fetchall()
        ]

    def get_data_by_app_and_date(
        self, app, earliest_date: Optional[str], latest_date: Optional[str]
    ) -> List[Record]:
        CONDITION = f" AND application LIKE '%{app}%'"
        my_command = self.base_command(
            self.date_filtering(earliest_date, latest_date) + CONDITION
        )
        print(my_command)
        conn = self.get_db_cursor()
        if earliest_date and latest_date:
            cursor = conn.execute(my_command, (earliest_date, latest_date))
        elif earliest_date:
            cursor = conn.execute(my_command, [earliest_date])
        elif latest_date:
            cursor = conn.execute(my_command, [latest_date])
        else:
            cursor = conn.execute(my_command)
        return [self.db_to_record(db_entry) for db_entry in cursor.fetchall()]


