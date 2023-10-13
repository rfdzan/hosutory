from subprocess import run
from webbrowser import open
from db.sql_query import update_fave
from db.search_db import query_the_db
import PySimpleGUI as sG


def search(query_the_db, values, window):
    data = query_the_db(values)
    result = []
    for item in data:
        result.append(item)
    window["-TABLE-"].update(values=result)
    window["prog"].update(value=f"Loaded {len(result)} songs.")
    return result


def add_fave(event, fave_key, result_dbquery, table_index, window, values):
    if event == fave_key[0]:
        mark = "*"
    else:
        mark = ""
    id_num = result_dbquery[table_index[0]][4]
    data = {"favorite": mark, "id": id_num}
    update_fave(data)
    _ = search(query_the_db, values, window)  # return value never updates context menu.


def to_clipboard(event, result_dbquery, table_index):
    copy_prefix = {"Copy::rCopy": "", "Copy Munix::rMunix": "+p "}
    try:
        to_copy = (
            f"{copy_prefix.get(event)}"
            f"{result_dbquery[table_index[0]][0]} {result_dbquery[table_index[0]][1]}"
        )
        run(["clip.exe"], input=to_copy.encode("utf-8"))
    except UnboundLocalError:
        sG.popup("No track selected!")


def preview_song(result_dbquery, table_index):
    try:
        web_link = result_dbquery[table_index[0]][5]
        open(web_link, new=2)
    except UnboundLocalError:
        sG.popup("No track selected!")


def context_menu(event, result_dbquery, table_index, window, values):
    if event in ("Copy::rCopy", "Copy Munix::rMunix"):
        to_clipboard(event, result_dbquery, table_index)

    if event == "Preview::rPreview":
        preview_song(result_dbquery, table_index)

    fave_key = ("Mark as Favorite::markFav", "Remove from Favorite::delFav")
    if event in fave_key:
        add_fave(event, fave_key, result_dbquery, table_index, window, values)
