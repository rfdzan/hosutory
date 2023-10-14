import PySimpleGUI as sG
from db.search_db import query_the_db
from db_gui_elements.elements import LeftCol, RightCol
from db_gui_elements.gui_logic import Logic


def main():
    layout_l = [LeftCol.text_result, LeftCol.table]
    layout_r = [
        RightCol.text_where,
        RightCol.choice_radios,
        RightCol.sort_radios,
        RightCol.text_like,
        RightCol.search_box,
        RightCol.button_search,
        RightCol.progress,
    ]

    layout = [
        [
            sG.Col(layout_l, vertical_alignment="Top"),
            sG.VerticalSeparator(color="white"),
            sG.Col(layout_r, vertical_alignment="Top"),
        ]
    ]
    logic = Logic()
    window = sG.Window("Search", layout)

    while True:
        event, values = window.read()
        if event == sG.WIN_CLOSED:
            break

        if event == "Search":
            logic.search(query_the_db, values, window)

        if event == "Clear":
            window["-INPUT-"].update(value="")

        if isinstance(event, tuple):
            if event[0] == "-TABLE-":
                index = event[2]  # ('-TABLE-', '+CLICKED+', (row, col))

        if "index" in locals():
            logic.context_menu(event, index, window, values)

    window.close()


if __name__ == "__main__":
    main()
