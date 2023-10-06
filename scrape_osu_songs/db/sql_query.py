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


def raise_error() -> None:
    raise ValueError("Keyword(s) doesn't exist. Keywords: 'artist', 'title', 'preview'")


def sanitize_input():
    choice = ("artist", "title", "preview", ",")
    select = input("select: ")
    if "," in select:
        select = select.split(",")
        for word in select:
            if word.strip() not in choice:
                raise_error()
    else:
        if select.strip() not in choice:
            raise_error()

    by = input("where: ")
    if by not in choice:
        raise_error()
    like = input("like: ")

    return select, by, like


def query_the_db():
    select, by, like = sanitize_input()
    if isinstance(select, list):
        select_strip = [word.strip() for word in select]
        select = ", ".join(select_strip)
    q_select = f"SELECT {select} FROM songs WHERE {by} LIKE :like"
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute(q_select, {"like": f"%{like}%"})
        for data in cursor:
            print(data)
