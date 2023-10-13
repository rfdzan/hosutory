from collections.abc import Generator

from .sql_query import connect


def raise_error() -> None:
    raise ValueError("Keyword(s) doesn't exist. Keywords: 'artist', 'title', 'preview'")


def sanitize_input():
    choice = ("artist", "title", "preview", "source")

    by = input("where: ")
    if by not in choice:
        raise_error()

    like = input("like: ")

    return choice, by, like


def query_the_db(values: dict[str, str | bool]) -> Generator[list[str]]:
    header = ("artist", "title", "preview", "source", "sort_artist", "sort_title")
    for key, value in values.items():
        if key in header:
            if value and "sort" in key:
                sort = key.split("_")[1]
            elif value:
                by = key
    like = values.get("-INPUT-")
    if values.get("-EXACT-"):
        q_select = (
            f"SELECT artist, title, source, favorite, id, preview FROM songs "
            f"WHERE {by} = :like ORDER BY {sort}"
        )
        like_query = like
    else:
        q_select = (
            f"SELECT artist, title, source, favorite, id, preview FROM songs "
            f"WHERE {by} LIKE :like ORDER BY {sort}"
        )
        like_query = f"%{like}%"

    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute(q_select, {"like": like_query})
        for data in cursor:
            yield [data[0], data[1], data[2], data[3], data[4], f"https:{data[5]}"]
