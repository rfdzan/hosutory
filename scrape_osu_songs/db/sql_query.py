import sqlite3
from pathlib import PurePath

DB_DIR = PurePath(__file__).parents[0]
DB_FILE = DB_DIR.joinpath("database_file", "osu_songs.db")


def connect() -> sqlite3.Connection:
    return sqlite3.connect(DB_FILE)


def create_tables() -> None:
    q_create_tables = """CREATE TABLE IF NOT EXISTS songs(
    id INTEGER PRIMARY KEY,
    artist TEXT,
    title TEXT,
    preview TEXT
    )STRICT
    """

    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute(q_create_tables)


def insert_into_db(data: list[dict]) -> None:
    q_insert_into_songs = """INSERT OR IGNORE INTO songs(
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
        cursor.executemany(q_insert_into_songs, data)
        conn.commit()


if __name__ == "__main__":
    pass
