import sqlite3

import pytest

from hosutory.db.sql_query import connect
from hosutory.scrape import make_request


def test_make_request():
    with pytest.raises(ValueError):
        make_request(-45, 100, None)


def test_connect():
    # database must always be successfully connected
    try:
        connect()
    except (sqlite3.Error, sqlite3.Warning) as e:
        print(e)
        raise ValueError("Database Connection Failed")
