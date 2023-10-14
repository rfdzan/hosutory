import PySimpleGUI as sG
from scrape import SONG_DIR, make_request, parse_and_save, save_song
from scrape_gui_elements.elements import ScrapeGUI
from scrape_gui_elements.gui_logic import main_logic


def main():
    layout = [
        ScrapeGUI.text_id,
        ScrapeGUI.user_id,
        ScrapeGUI.start_stop,
        ScrapeGUI.json_dbstore,
        ScrapeGUI.start_procedure,
        ScrapeGUI.text_progress,
        ScrapeGUI.progress,
        ScrapeGUI.text_progress_db,
        ScrapeGUI.progress_db,
    ]

    window = sG.Window("Scrape", layout=layout)

    while True:
        event, values = window.read()
        if event == sG.WIN_CLOSED:
            break
        if event == "Start":
            main_logic(
                values, window, make_request, save_song, parse_and_save, SONG_DIR
            )
        window["-PROGTXT-"].update("No downloads.")
        window["-PROGTXTDB-"].update("No database task.")
        window["-PROGRESS-"].update(current_count=0)
        window["-PROGDB-"].update(current_count=0)
    window.close()


if __name__ == "__main__":
    main()
