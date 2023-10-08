import PySimpleGUI as sG
from scrape_osu_songs.db.search_db import query_the_db

def main():
    sG.theme("SystemDefaultForReal")
    sG.Titlebar("Search songs", background_color="Black")
    # left_window
    text_result = [sG.Text("Result:")]
    table = [sG.Table(values=["" for _ in range(4)], expand_x=True, num_rows=10, justification="left" ,headings=["artist", "title", "preview", "source"],key="-TABLE-")]
    # right_window
    text_where = [sG.Text("Where:")]
    choice_radios = [
        sG.Radio("Artist", 1, default=True, key="artist"),
        sG.Radio("Title", 1, key="title"),
        sG.Radio("Preview", 1, key="preview"),
        sG.Radio("Source", 1, key="source"),
    ]
    text_like = [sG.Text("Like:")]
    search_box = [sG.InputText("Miku", key="-INPUT-")]
    button_search = [
        sG.Button("Search", mouseover_colors="white"),
        sG.Button("Clear", mouseover_colors="white"),
    ]
    # layouts
    layout_l = [text_result, table]
    layout_r = [text_where, choice_radios, text_like, search_box, button_search]

    layout = [[sG.Col(layout_l, vertical_alignment="Top"), sG.Col(layout_r, vertical_alignment="Top")]]

    window = sG.Window("Search", layout, finalize=True, resizable=True)

    while True:
        event, values = window.read()
        if event == sG.WIN_CLOSED:
            break
        if event == "Search":
            result = query_the_db(values)
            window["-TABLE-"].update(values=result)
        if event == "Clear":
            window["-TABLE-"].update(values=["" for _ in range(4)])
    window.close()


if __name__ == "__main__":
    main()
