import PySimpleGUI as sG
import scrape
from pathlib import Path


def get_values(values: dict[str, str | bool]):
    user_id = values.get("-ID-")
    idx_start = values.get("-INDEXSTART-")
    idx_stop = values.get("-INDEXSTOP-")
    store_db = values.get("-STOREDB-")
    return user_id, idx_start, idx_stop, store_db


def process_request(values: dict[str, str | bool], window):
    user_id, idx_start, idx_stop, store_db = get_values(values)
    window["-PROGTXT-"].update(value=f"Downloading {int(int(idx_stop)//100)} files")
    for value in scrape.save_song(int(user_id), int(idx_start), int(idx_stop)):
        window["-PROGRESS-"].update(current_count=value, max=idx_stop)
    if store_db:
        num_file = [filepath for filepath in Path(scrape.SONG_DIR).iterdir()]
        window["-PROGTXTDB-"].update(value="Saving to database...")
        for value in scrape.parse_and_save():
            window["-PROGDB-"].update(current_count=value, max=len(num_file) - 1)
        window["-PROGTXTDB-"].update(value="Database task done!")


def sanitize_input(values: dict[str, str | bool]):
    user_id, idx_start, idx_stop, store_db = get_values(values)
    try:
        user_id = int(user_id)
        idx_start = int(idx_start)
        idx_stop = int(idx_stop)
        return True
    except (TypeError, ValueError):
        sG.Popup(
            "All input fields only accept integers and must be populated.",
            title="Warning",
        )
        return False


def main():
    sG.theme("SystemDefaultForReal")
    text_id = [sG.Text("ID:")]
    user_id = [sG.InputText("", key="-ID-")]
    start_stop = [
        sG.Text("start:"),
        sG.InputText("0", size=(10, 10), key="-INDEXSTART-"),
        sG.Text("stop:"),
        sG.InputText("", size=(10, 10), key="-INDEXSTOP-"),
    ]
    json_dbstore = [
        sG.Checkbox("Store JSON to Database", default=True, key="-STOREDB-")
    ]
    start_procedure = [sG.Button("Start")]
    text_progress = [sG.Text("No downloads.", key="-PROGTXT-")]
    progress = [sG.ProgressBar(100, orientation="h", size=(30, 10), key="-PROGRESS-")]
    text_progress_db = [sG.Text("No database task.", key="-PROGTXTDB-")]
    progress_db = [sG.ProgressBar(100, orientation="h", size=(30, 10), key="-PROGDB-")]

    layout = [
        text_id,
        user_id,
        start_stop,
        json_dbstore,
        start_procedure,
        text_progress,
        progress,
        text_progress_db,
        progress_db,
    ]

    window = sG.Window("Scrape", layout=layout)

    while True:
        event, values = window.read()
        print(event)
        print(values)
        if event == sG.WIN_CLOSED:
            break
        if event == "Start":
            if sanitize_input(values):
                process_request(values, window)
        window["-PROGTXT-"].update("No downloads.")
        window["-PROGTXTDB-"].update("No database task.")
        window["-PROGRESS-"].update(current_count=0)
        window["-PROGDB-"].update(current_count=0)
    window.close()


if __name__ == "__main__":
    main()
