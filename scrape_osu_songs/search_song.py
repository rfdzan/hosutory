from db.search_db import query_the_db

while True:
    try:
        print("Keywords: 'artist', 'title', 'preview'")
        query_the_db()
    except ValueError as err:
        print(err)
