from pathlib import PurePath
from subprocess import run

song_search = PurePath(__file__).parents[0].joinpath("gui.py")
python = PurePath(__file__).parents[0].joinpath(".venv", "Scripts", "python.exe")
run([python, song_search])
