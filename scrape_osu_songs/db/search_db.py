from tabulate import tabulate

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


def query_the_db():
    select, by, like = sanitize_input()
    header = select
    q_select = f"SELECT artist, title, preview, source FROM songs WHERE {by} LIKE :like ORDER BY title"

    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute(q_select, {"like": f"%{like}%"})
        table = [(data[0], data[1], f"https:{data[2]}", data[3]) for data in cursor]

    print(tabulate(table, headers=header, tablefmt="grid"))