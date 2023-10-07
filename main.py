from subprocess import Popen, run
from pathlib import PurePath

song_search = (
    PurePath(__file__).parents[0].joinpath("scrape_osu_songs", "search_song.py")
)
python = PurePath(__file__).parents[0].joinpath(".venv", "Scripts", "python.exe")
run([python, song_search])
