from pathlib import PurePath
from subprocess import run
from sys import platform

start_gui = PurePath(__file__).parents[0].joinpath("hosutory", "project.py")
python = PurePath(__file__).parents[0].joinpath(".venv", "Scripts", "python.exe")
if platform == "linux":
    python = PurePath(__file__).parents[0].joinpath(".venv", "bin", "python")
run([python, start_gui])
