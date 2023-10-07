from scrape_osu_songs.db.search_db import query_the_db


def main():
    while True:
        try:
            query_the_db()
        except ValueError as err:
            print(err)


if __name__ == '__main__':
    main()
