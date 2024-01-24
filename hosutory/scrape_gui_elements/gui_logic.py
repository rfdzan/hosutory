from collections.abc import Callable
from pathlib import Path, PurePath
from threading import Thread

import PySimpleGUI as sG


def id_exists(values: dict[str, str | bool], make_request: Callable):
    user_id, _, _, _ = get_values(values)
    try:
        _ = make_request(user_id, 100, header=None)
        return True
    except ValueError as err:
        sG.popup(err, title="Error")
        return False


def get_values(values: dict[str, str | bool]):
    user_id = values.get("-ID-")
    idx_start = values.get("-INDEXSTART-")
    idx_stop = values.get("-INDEXSTOP-")
    store_db = values.get("-STOREDB-")
    return user_id, idx_start, idx_stop, store_db


def process_request(
    values: dict[str, str | bool],
    window,
    save_song: Callable,
    parse_and_save: Callable,
    SONG_DIR: PurePath,
):
    user_id, idx_start, idx_stop, store_db = get_values(values)

    for value in save_song(abs(int(user_id)), abs(int(idx_start)), abs(int(idx_stop))):
        window["-PROGTXT-"].update(
            value=f"Downloading {int(value // 100)} "
            f"of {int(int(idx_stop) // 100)} files"
        )
        window["-PROGRESS-"].update(current_count=value, max=idx_stop)
    window["-PROGTXT-"].update(value="Finished downloading files!")
    if store_db:
        num_file = [filepath for filepath in Path(SONG_DIR).iterdir()]
        window["-PROGTXTDB-"].update(value="Saving to database...")
        for value in parse_and_save():
            window["-PROGDB-"].update(current_count=value, max=len(num_file) - 1)
        window["-PROGTXTDB-"].update(value="Database task done!")


def sanitize_input(values: dict[str, str | bool]):
    user_id, idx_start, idx_stop, store_db = get_values(values)
    try:
        _ = int(user_id)
        idx_start = int(idx_start)
        idx_stop = int(idx_stop)
    except (TypeError, ValueError):
        sG.Popup(
            "All input fields only accept integers and must be populated.",
            title="Warning",
        )
        return False
    if idx_start > idx_stop:
        sG.Popup("'start' MUST be smaller than 'stop'", title="Warning")
        return False
    return True


def main_logic(values, window, make_request, save_song, parse_and_save, SONG_DIR):
    if sanitize_input(values):
        check = id_exists(values, make_request)
        if check:
            task = Thread(
                group=None,
                target=process_request,
                args=(values, window, save_song, parse_and_save, SONG_DIR),
            )
            task.start()
