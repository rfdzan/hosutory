from pathlib import PurePath
from subprocess import run

start_gui = PurePath(__file__).parents[0].joinpath("scrape_osu_songs", "scrape_gui.py")
python = PurePath(__file__).parents[0].joinpath(".venv", "Scripts", "python.exe")
run([python, start_gui])
