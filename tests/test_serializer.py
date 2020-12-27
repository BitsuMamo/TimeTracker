from datetime import datetime
from time_tracker.serializer import AppDB
import sqlite3

sample_data = [
    ("VS Code", "2020-02-10T22:55:13-08:00", "2020-02-10T23:15:13-08:00"),
    ("VS Code", "2020-01-05T22:55:13-08:00", "2020-01-05T23:25:13-08:00"),
    ("Horizon: Zero Dawn", "2019-08-02T18:32:21-08:00", "2019-08-02T18:32:22-08:00"),
    ("Firefox", "2012-11-09T10:35:10-08:00", "2012-11-09T10:45:21-08:00"),
    ("Photoshop", "2008-08-04T01:20:43-08:00", "2008-08-04T01:24:05-08:00"),
]


def init_test_db() -> AppDB:
    with open("test.db", "w") as test_db:
        test_db.close()
    conn = sqlite3.connect("test.db")
    db = AppDB(conn)
    db.init_db(conn)
    return db


def test_db_read_write() -> None:
    db = init_test_db()
    formatted_data = [
        (entry[0], datetime.fromisoformat(entry[1]), datetime.fromisoformat(entry[2]))
        for entry in sample_data
    ]
    db.save(formatted_data)
    data = db.get_all_data()
    assert len(data) == len(sample_data)
    assert set(
        [(entry[0], entry[1].isoformat(), entry[2].isoformat()) for entry in data]
    ) == set(sample_data)


def test_db_get_by_app() -> None:
    db = init_test_db()
    formatted_data = [
        (entry[0], datetime.fromisoformat(entry[1]), datetime.fromisoformat(entry[2]))
        for entry in sample_data
    ]
    db.save(formatted_data)
    data_1 = db.get_data_by_app("VS Code")
    data_2 = db.get_data_by_app("Mario")
    assert len(data_1) == 2
    assert len(data_2) == 0
    assert set(
        [(entry[0], entry[1].isoformat(), entry[2].isoformat()) for entry in data_1]
    ) == set(sample_data[:2])


def test_db_get_by_date() -> None:
    db = init_test_db()
    formatted_data = [
        (entry[0], datetime.fromisoformat(entry[1]), datetime.fromisoformat(entry[2]))
        for entry in sample_data
    ]
    db.save(formatted_data)
    data_1 = db.get_data_by_date(earliest_date="2012-11-10T10:45:21-08:00")
    data_2 = db.get_data_by_date(latest_date="2020-01-01T22:55:13-08:00")
    data_3 = db.get_data_by_date(
        earliest_date="2010-11-10T10:45:21-08:00",
        latest_date="2020-02-01T22:55:13-08:00",
    )
    data_4 = db.get_data_by_date(latest_date=datetime.now().isoformat())
    data_5 = db.get_data_by_date(earliest_date="2000-01-01T22:55:13-08:00")
    assert set(
        [(entry[0], entry[1].isoformat(), entry[2].isoformat()) for entry in data_1]
    ) == set(sample_data[:3])
    assert set(
        [(entry[0], entry[1].isoformat(), entry[2].isoformat()) for entry in data_2]
    ) == set(sample_data[2:])
    assert set(
        [(entry[0], entry[1].isoformat(), entry[2].isoformat()) for entry in data_3]
    ) == set(sample_data[1:4])
    assert set(
        [(entry[0], entry[1].isoformat(), entry[2].isoformat()) for entry in data_4]
    ) == set(sample_data)
    assert set(
        [(entry[0], entry[1].isoformat(), entry[2].isoformat()) for entry in data_5]
    ) == set(sample_data)
