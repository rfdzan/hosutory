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


def query_the_db(values: dict[str, str]) -> Generator[list[str]]:
    header = ("artist", "title", "preview", "source")
    for key, value in values.items():
        if key in header:
            if value:
                by = key
                break
    like = values.get("-INPUT-")

    q_select = (
        f"SELECT artist, title, preview, source FROM songs "
        f"WHERE {by} LIKE :like ORDER BY title"
    )

    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute(q_select, {"like": f"%{like}%"})
        for data in cursor:
            yield [data[0], data[1], data[3], f"https:{data[2]}"]
