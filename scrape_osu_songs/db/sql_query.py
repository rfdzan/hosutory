import sqlite3
from pathlib import PurePath

DB_DIR = PurePath(__file__).parents[0]
DB_FILE = DB_DIR.joinpath("database_file", "osu_songs.db")
test_db = DB_DIR.joinpath("database_file", "test.db")


def connect() -> sqlite3.Connection:
    return sqlite3.connect(DB_FILE)


def create_tables() -> None:
    q_create_tables = """CREATE TABLE IF NOT EXISTS songs(
    id INTEGER PRIMARY KEY,
    artist TEXT,
    title TEXT,
    preview TEXT UNIQUE,
    source TEXT,
    favorite TEXT DEFAULT ''
    )STRICT
    """
    q_wal_mode = "PRAGMA journal_mode=wal"
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute(q_create_tables)
        cursor.execute(q_wal_mode)


def update_fave(data):
    q_update_fave = """UPDATE OR IGNORE songs
    SET favorite = :favorite
    WHERE id = :id
    """
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute(q_update_fave, data)


def insert_into_db(data: list[dict]) -> None:
    q_insert_into_songs = """INSERT OR IGNORE INTO songs(
    artist,
    title,
    preview,
    source
    ) VALUES(
    :artist,
    :title,
    :preview,
    :source
    )
    """
    with connect() as conn:
        cursor = conn.cursor()
        cursor.executemany(q_insert_into_songs, data)
        conn.commit()
