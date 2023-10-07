import json
from collections.abc import Generator
from pathlib import Path, PurePath

import httpx
from tqdm import tqdm

from db.sql_query import insert_into_db

PROJ_DIR = PurePath(__file__).parents[0]
HEADERS = PROJ_DIR.joinpath("headers.json")
SONG_DIR = PROJ_DIR.joinpath("songs")


def make_request(offset: int) -> list[dict]:
    url = f"https://osu.ppy.sh/users/4836880/beatmapsets/most_played?limit=100&offset={offset}"
    with open(HEADERS) as file:
        header = json.load(file)
    response = httpx.get(url, headers=header)
    return response.json()


def save_song() -> None:
    for offset in range(0, 3900, 100):  # total number of song is 3889
        response = make_request(offset)
        with open(PROJ_DIR.joinpath(f"songs{int(offset / 100)}.json"), "w") as file:
            json.dump(response, file)


def parse() -> Generator[dict[str], None, None]:
    for file in tqdm(Path(SONG_DIR).iterdir()):
        with open(SONG_DIR.joinpath(file)) as file:
            song = json.load(file)
        for item in song:
            beatmapset = item.get("beatmapset")
            artist = beatmapset.get("artist")
            title = beatmapset.get("title")
            preview = beatmapset.get("preview_url")
            yield {"artist": artist, "title": title, "preview": preview}


def store_songs() -> None:
    complete_data = [data for data in parse()]
    insert_into_db(complete_data)


if __name__ == "__main__":
    store_songs()
