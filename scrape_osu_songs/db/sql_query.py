import sqlite3
from pathlib import PurePath

DB_DIR = PurePath(__file__).parents[0]
DB_FILE = DB_DIR.joinpath("database_file", "osu_songs.db")


def connect() -> sqlite3.Connection:
    return sqlite3.connect(DB_FILE)


def create_tables() -> None:
    Q_CREATE_TABLES = """CREATE TABLE IF NOT EXISTS songs(
    id INTEGER PRIMARY KEY,
    artist TEXT,
    title TEXT,
    preview TEXT
    )STRICT
    """

    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute(Q_CREATE_TABLES)


def insert_into_db(data: list[dict]) -> None:
    Q_INSERT_INTO_SONGS = """INSERT OR IGNORE INTO songs(
    artist,
    title,
    preview
    ) VALUES(
    :artist,
    :title,
    :preview
    )
    """
    with connect() as conn:
        cursor = conn.cursor()
        cursor.executemany(Q_INSERT_INTO_SONGS, data)
        conn.commit()


if __name__ == "__main__":
    pass
