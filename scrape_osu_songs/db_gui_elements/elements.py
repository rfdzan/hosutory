from dataclasses import dataclass

import PySimpleGUI as sG

sG.theme("SystemDefaultForReal")
sG.Titlebar("Search songs", background_color="Black")


@dataclass
class LeftCol:
    text_result = [sG.Text("Result:")]
    table = [
        sG.Table(
            values=[["" for _ in range(4)]],
            num_rows=10,
            max_col_width=1000,
            auto_size_columns=False,
            vertical_scroll_only=False,
            justification="left",
            headings=["artist", "title", "source", "fav"],
            enable_click_events=True,
            right_click_selects=True,
            right_click_menu=[
                "&Right",
                [
                    "Copy::rCopy",
                    "Copy Munix::rMunix",
                    "Mark as Favorite::markFav",
                    "Remove from Favorite::delFav",
                    "Preview::rPreview",
                ],
            ],
            key="-TABLE-",
        )
    ]


@dataclass
class RightCol:
    text_where = [sG.Text("Where:")]
    choice_radios = [
        sG.Radio("Artist", 1, default=True, key="artist"),
        sG.Radio("Title", 1, key="title"),
        sG.Radio("Source", 1, key="source"),
        sG.Checkbox("Exact?", default=False, key="-EXACT-"),
    ]
    sort_radios = [
        sG.Text("Sort by:"),
        sG.Radio("Artist", 2, key="sort_artist"),
        sG.Radio("Title", 2, default=True, key="sort_title"),
        sG.Radio("Favorite", 2, key="sort_favorite"),
    ]
    text_like = [sG.Text("Like:")]
    search_box = [sG.InputText("", key="-INPUT-")]
    button_search = [
        sG.Button("Search", mouseover_colors="white", bind_return_key=True),
        sG.Button("Clear", mouseover_colors="white"),
    ]
    progress = [sG.Text(text="", key="prog")]
