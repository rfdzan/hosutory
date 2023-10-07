import json
from collections.abc import Generator
from pathlib import Path, PurePath
from time import sleep

import httpx
from tqdm import tqdm

from db.sql_query import insert_into_db

PROJ_DIR = PurePath(__file__).parents[0]
HEADERS = PROJ_DIR.joinpath("headers.json")
SONG_DIR = PROJ_DIR.joinpath("songs")


def make_request(user_id: int, offset: int) -> list[dict]:
    url = f"https://osu.ppy.sh/users/{user_id}/beatmapsets/most_played?limit=100&offset={offset}"
    with open(HEADERS) as file:
        header = json.load(file)
    while True:
        try:
            response = httpx.get(url, headers=header)
            return response.json()
        except (httpx.TimeoutException, json.decoder.JSONDecodeError):
            for i in range(30, 0):
                print(
                    f"encountered an error in make_request(), retrying in {i} seconds",
                    end="\r",
                )
                sleep(1)


def save_song(user_id: int, start: int, stop: int) -> None:
    user_id = str(user_id)
    user_id_folder = SONG_DIR.joinpath(user_id)
    if not Path(user_id_folder).exists():
        Path(user_id_folder).mkdir()
    for offset in tqdm(range(start, stop + 100, 100)):
        response = make_request(user_id, offset)
        with open(
            user_id_folder.joinpath(f"songs{int(offset / 100)}.json"), "w"
        ) as file:
            json.dump(response, file)


def parse(user_id: int) -> Generator[dict[str], None, None]:
    user_id = str(user_id)
    user_id_folder = SONG_DIR.joinpath(user_id)
    for file in tqdm(Path(user_id_folder).iterdir()):
        with open(user_id_folder.joinpath(file), encoding="utf-8") as file:
            song = json.load(file)
        for item in song:
            beatmapset = item.get("beatmapset")
            artist = beatmapset.get("artist")
            title = beatmapset.get("title")
            preview = beatmapset.get("preview_url")
            source = beatmapset.get("source")
            yield {
                "artist": artist,
                "title": title,
                "preview": preview,
                "source": source,
            }


def store_songs(user_id: int) -> None:
    complete_data = [data for data in parse(user_id)]
    insert_into_db(complete_data)


def parse_and_save():
    for filename in Path(SONG_DIR).iterdir():
        store_songs(filename.name)


if __name__ == "__main__":
    parse_and_save()
    pass
