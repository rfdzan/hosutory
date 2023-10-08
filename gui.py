from subprocess import run
from webbrowser import open

import PySimpleGUI as sG

from scrape_osu_songs.db.search_db import query_the_db


def left_Col():
    text_result = [sG.Text("Result:")]
    table = [
        sG.Table(
            values=["" for _ in range(4)],
            num_rows=10,
            max_col_width=1000,
            auto_size_columns=False,
            vertical_scroll_only=False,
            justification="left",
            headings=["artist", "title", "source"],
            enable_click_events=True,
            right_click_selects=True,
            right_click_menu=[
                "&Right",
                ["Copy::rCopy", "Copy Munix::rMunix", "Preview::rPreview"],
            ],
            key="-TABLE-",
        )
    ]
    return text_result, table


def right_Col():
    text_where = [sG.Text("Where:")]
    choice_radios = [
        sG.Radio("Artist", 1, default=True, key="artist"),
        sG.Radio("Title", 1, key="title"),
        sG.Radio("Source", 1, key="source"),
    ]
    text_like = [sG.Text("Like:")]
    search_box = [sG.InputText("Miku", key="-INPUT-")]
    button_search = [
        sG.Button("Search", mouseover_colors="white"),
        sG.Button("Clear", mouseover_colors="white"),
    ]
    progress = [sG.Text(text="", key="prog")]

    return text_where, choice_radios, text_like, search_box, button_search, progress


def main():
    sG.theme("SystemDefaultForReal")
    sG.Titlebar("Search songs", background_color="Black")
    # left_window
    text_result, table = left_Col()
    # right_window
    (
        text_where,
        choice_radios,
        text_like,
        search_box,
        button_search,
        progress,
    ) = right_Col()
    # layouts
    layout_l = [text_result, table]
    layout_r = [
        text_where,
        choice_radios,
        text_like,
        search_box,
        button_search,
        progress,
    ]

    layout = [
        [
            sG.Col(layout_l, vertical_alignment="Top"),
            sG.Col(layout_r, vertical_alignment="Top"),
        ]
    ]

    window = sG.Window("Search", layout)

    while True:
        event, values = window.read()
        if event == sG.WIN_CLOSED:
            break
        if event == "Search":
            data = query_the_db(values)
            result = []
            for item in data:
                result.append(item)
            window["-TABLE-"].update(values=result)
            window["prog"].update(value=f"Loaded {len(result)} songs.")
        if event == "Clear":
            window["-TABLE-"].update(values=["" for _ in range(4)])
        if isinstance(event, tuple):
            if event[0] == "-TABLE-":
                index = event[2]

        if event in ("Copy::rCopy", "Copy Munix::rMunix"):
            copy_prefix = {"Copy::rCopy": "", "Copy Munix::rMunix": "+p "}
            try:
                to_copy = (
                    f"{copy_prefix.get(event)}"
                    f"{result[index[0]][0]} {result[index[0]][1]}"
                )
                run(["clip.exe"], input=to_copy.encode("utf-8"))
            except UnboundLocalError:
                sG.popup("No track selected!")
        if event == "Preview::rPreview":
            try:
                web_link = result[index[0]][3]
                open(web_link, new=2)
            except UnboundLocalError:
                sG.popup("No track selected!")

    window.close()


if __name__ == "__main__":
    main()
