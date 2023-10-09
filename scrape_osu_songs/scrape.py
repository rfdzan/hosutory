import json
from collections.abc import Generator
from pathlib import Path, PurePath
from time import sleep

import httpx

from db.sql_query import insert_into_db

PROJ_DIR = PurePath(__file__).parents[0]
HEADERS = PROJ_DIR.joinpath("headers.json")
SONG_DIR = PROJ_DIR.joinpath("songs")


def mkdir_songs() -> None:
    if not Path(SONG_DIR).exists():
        Path.mkdir(SONG_DIR)


def make_request(user_id: str, offset: int, max: int) -> list[dict]:
    url = f"https://osu.ppy.sh/users/{user_id}/beatmapsets/most_played?limit=100&offset={offset}"
    with open(HEADERS) as file:
        header = json.load(file)
    while True:
        try:
            response = httpx.get(url, headers=header)
            for data in response.json():
                if data == "error":
                    raise ValueError(f"No data for ID: {user_id}")
                return response.json()
        except httpx.HTTPError:
            for i in range(30, 0):
                print(
                    f"encountered an error in make_request(), retrying in {i} seconds",
                    end="\r",
                )
                sleep(1)
        except json.decoder.JSONDecodeError:
            if offset == max:
                break
            continue


def save_song(user_id_int: int, start: int, stop: int) -> Generator[int, None, None]:
    mkdir_songs()
    user_id = str(user_id_int)
    user_id_folder = SONG_DIR.joinpath(user_id)
    if not Path(user_id_folder).exists():
        Path(user_id_folder).mkdir()
    for offset in range(start, stop + 100, 100):
        response = make_request(user_id, offset, max=stop)
        with open(
            user_id_folder.joinpath(f"songs{int(offset / 100)}.json"), "w"
        ) as file:
            json.dump(response, file)
        yield offset


def parse(user_id: str) -> Generator[dict[str, str], None, None]:
    mkdir_songs()
    user_id_folder = SONG_DIR.joinpath(user_id)
    for file in Path(user_id_folder).iterdir():
        with open(user_id_folder.joinpath(file), encoding="utf-8") as file:
            song = json.load(file)
        if song is None:
            continue
        for item in song:
            try:
                beatmapset = item.get("beatmapset")
            except AttributeError:
                continue
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
    complete_data = [data for data in parse(str(user_id))]
    insert_into_db(complete_data)


def parse_and_save() -> Generator[int, None, None]:
    mkdir_songs()
    for idx, filename in enumerate(Path(SONG_DIR).iterdir()):
        store_songs(filename.name)
        yield idx
