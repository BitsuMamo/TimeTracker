from datetime import datetime
import pytest
import sqlite3
from time_tracker import serializer

sample_data = [
    ("VS Code", "2020-02-10T22:55:13-08:00", "2020-02-10T23:15:13-08:00"),
    ("Horizon: Zero Dawn", "2019-08-02T18:32:21-08:00", "2019-08-02T18:32:22-08:00"),
    ("Firefox", "2012-11-09T10:35:10-08:00", "2012-11-09T10:45:21-08:00"),
    ("Photoshop", "2008-08-04T01:20:43-08:00", "2008-08-04T01:24:05-08:00"),
]


def init_test_db() -> sqlite3.Connection:
    with open("test.db", "w") as test_db:
        test_db.close()
    serializer.m_db_con = sqlite3.connect("test.db")
    serializer.init_db(serializer.m_db_con)
    return serializer.m_db_con


def test_db_read_write() -> None:
    init_test_db()
    formatted_data = [
        (entry[0], datetime.fromisoformat(entry[1]), datetime.fromisoformat(entry[2]))
        for entry in sample_data
    ]
    serializer.save_to_db(formatted_data)
    data = serializer.get_all_data()
    assert len(data) == 4
    assert set([(entry[0], entry[1], entry[2]) for entry in data]) == set(sample_data)

