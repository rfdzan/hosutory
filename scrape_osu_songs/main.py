import json
from pathlib import PurePath, Path
import httpx


PROJ_DIR = PurePath(__file__).parents[0]
HEADERS = PROJ_DIR.joinpath("headers.json")
SONG_DIR = PROJ_DIR.joinpath("songs")


def make_request(offset: int):
    url = f"https://osu.ppy.sh/users/4836880/beatmapsets/most_played?limit=100&offset={offset}"
    response = httpx.get(url)
    return response.json()


def save_song():
    for offset in range(3800, 5100, 100):
        response = make_request(offset)
        with open(PROJ_DIR.joinpath(f"songs{int(offset / 100)}.json"), "w") as file:
            json.dump(response, file)


def parse():
    with open(SONG_DIR.joinpath("songs38.json")) as file:
        read = json.load(file)
    print(len(read))


if __name__ == "__main__":
    parse()
    pass
