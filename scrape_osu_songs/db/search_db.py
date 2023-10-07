from sql_query import connect


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
